import scipy.sparse as sp
import tensorflow as tf
from tensorflow.keras import Input
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.losses import SparseCategoricalCrossentropy

from graphgallery.nn.layers.tensorflow import DenseConvolution, Gather
from graphgallery.gallery import GalleryModel
from graphgallery.sequence import FullBatchSequence
from graphgallery import functional as gf
from graphgallery.nn.models import TFKeras


class SAT(GalleryModel):
    def __init__(self,
                 graph,
                 adj_transform="normalize_adj",
                 attr_transform=None,
                 K=35,
                 graph_transform=None,
                 device="cpu",
                 seed=None,
                 name=None,
                 **kwargs):
        r"""Create a Graph Convolutional Networks (GCN) model
            using Spetral Adversarial Training (SAT) defense strategy.

        This can be instantiated in the following way:

            model = SAT(graph)
                with a `graphgallery.data.Graph` instance representing
                A sparse, attributed, labeled graph.

        Parameters:
        ----------
        graph: An instance of `graphgallery.data.Graph`.
            A sparse, attributed, labeled graph.
        adj_transform: string, `transform`, or None. optional
            How to transform the adjacency matrix. See `graphgallery.functional`
            (default: :obj:`'normalize_adj'` with normalize rate `-0.5`.
            i.e., math:: \hat{A} = D^{-\frac{1}{2}} A D^{-\frac{1}{2}}) 
        attr_transform: string, `transform`, or None. optional
            How to transform the node attribute matrix. See `graphgallery.functional`
            (default :obj: `None`)
        K: integer. optional.
            The number of eigenvalues and eigenvectors desired.
            `K` must be smaller than N-1. It is not possible to compute all
            eigenvectors of an adjacency matrix.
        graph_transform: string, `transform` or None. optional
            How to transform the graph, by default None.
        device: string. optional
            The device where the model is running on. 
            You can specified ``CPU``, ``GPU`` or ``cuda``  
            for the model. (default: :str: `cpu`, i.e., running on the `CPU`)
        seed: interger scalar. optional 
            Used in combination with `tf.random.set_seed` & `np.random.seed` 
            & `random.seed` to create a reproducible sequence of tensors across 
            multiple calls. (default :obj: `None`, i.e., using random seed)
        name: string. optional
            Specified name for the model. (default: :str: `class.__name__`)
        kwargs: other custom keyword parameters.
        """

        super().__init__(graph, device=device, seed=seed, name=name,
                         adj_transform=adj_transform,
                         attr_transform=attr_transform,
                         graph_transform=graph_transform,
                         **kwargs)

        self.register_cache("K", K)
        self.process()

    def process_step(self, re_decompose=False):
        graph = self.transform.graph_transform(self.graph)
        adj_matrix = self.transform.adj_transform(graph.adj_matrix)
        node_attr = self.transform.attr_transform(graph.node_attr)

        if re_decompose or not "U" in self.cache:
            V, U = sp.linalg.eigs(adj_matrix.astype('float64'), k=self.cache.K)
            U, V = U.real, V.real
        else:
            U, V = self.cache.U, self.cache.V

        adj_matrix = (U * V) @ U.T
        adj_matrix = self.transform.adj_transform(adj_matrix)

        with tf.device(self.device):
            X, A, U, V = gf.astensors(node_attr, adj_matrix, U, V,
                                      device=self.device)
        # ``A`` , ``X`` , U`` and ``V`` are cached for later use
        self.register_cache("X", X)
        self.register_cache("A", A)
        self.register_cache("U", U)
        self.register_cache("V", V)

    # use decorator to make sure all list arguments have the same length

    @gf.equal()
    def build(self,
              hiddens=[32],
              activations=['relu'],
              dropout=0.5,
              weight_decay=5e-4,
              lr=0.01,
              use_bias=False,
              eps1=0.3,
              eps2=1.2,
              lamb1=0.8,
              lamb2=0.8):

        with tf.device(self.device):

            x = Input(batch_shape=[None, self.graph.num_node_attrs],
                      dtype=self.floatx,
                      name='features')
            adj = Input(batch_shape=[None, None],
                        dtype=self.floatx,
                        name='adj_matrix')
            index = Input(batch_shape=[None], dtype=self.intx, name='index')

            h = x
            for hid, activation in zip(hiddens, activations):
                h = DenseConvolution(
                    hid,
                    use_bias=use_bias,
                    activation=activation,
                    kernel_regularizer=regularizers.l2(weight_decay))([h, adj])

                h = Dropout(rate=dropout)(h)

            h = DenseConvolution(self.graph.num_node_classes,
                                 use_bias=use_bias)([h, adj])
            h = Gather()([h, index])

            model = TFKeras(inputs=[x, adj, index], outputs=h)
            model.compile(loss=SparseCategoricalCrossentropy(from_logits=True),
                          optimizer=Adam(lr=lr),
                          metrics=['accuracy'])

            self.eps1 = eps1
            self.eps2 = eps2
            self.lamb1 = lamb1
            self.lamb2 = lamb2
            self.model = model

    @tf.function
    def train_step(self, sequence):
        (X, A, idx), y = next(iter(sequence))

        U, V = self.cache.U, self.cache.V
        model = self.model
        loss_fn = model.loss
        metric = model.metrics[0]
        optimizer = model.optimizer
        model.reset_metrics()

        with tf.GradientTape() as tape:
            tape.watch([U, V])
            A0 = (U * V) @ tf.transpose(U)
            output = model([X, A0, idx])
            loss = loss_fn(y, output)

        U_grad, V_grad = tape.gradient(loss, [U, V])
        U_grad = self.eps1 * U_grad / tf.norm(U_grad)
        V_grad = self.eps2 * V_grad / tf.norm(V_grad)

        U_hat = U + U_grad
        V_hat = V + V_grad

        with tf.GradientTape() as tape:
            A1 = (U_hat * V) @ tf.transpose(U_hat)
            A2 = (U * V_hat) @ tf.transpose(U)

            output0 = model([X, A0, idx])
            output1 = model([X, A1, idx])
            output2 = model([X, A2, idx])

            loss = loss_fn(y, output0) + tf.reduce_sum(model.losses)
            loss += self.lamb1 * loss_fn(y, output1) + self.lamb2 * loss_fn(
                y, output2)
            metric.update_state(y, output0)

        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        return gf.BunchDict(loss=loss, accuracy=metric.result())

    def train_sequence(self, index):
        labels = self.graph.node_label[index]
        with tf.device(self.device):
            sequence = FullBatchSequence(
                [self.cache.X, self.cache.A, index], labels)
        return sequence
