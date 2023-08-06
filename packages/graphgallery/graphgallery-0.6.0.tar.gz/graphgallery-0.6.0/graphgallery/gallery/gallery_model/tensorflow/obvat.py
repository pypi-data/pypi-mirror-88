import tensorflow as tf
from tensorflow.keras import Input
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.initializers import TruncatedNormal
from tensorflow.keras.losses import SparseCategoricalCrossentropy

from graphgallery.nn.layers.tensorflow import GraphConvolution, Gather
from graphgallery.gallery import GalleryModel
from graphgallery.sequence import FullBatchSequence
from graphgallery.utils.bvat_utils import kl_divergence_with_logit, entropy_y_x

from graphgallery import functional as gf
from graphgallery.nn.models import TFKeras


class OBVAT(GalleryModel):
    """
        Implementation of optimization-based Batch Virtual Adversarial Training 
        Graph Convolutional Networks (OBVAT).
        `Batch Virtual Adversarial Training for Graph Convolutional Networks 
        <https://arxiv.org/abs/1902.09192>`
        Tensorflow 1.x implementation: <https://github.com/thudzj/BVAT>

    """

    def __init__(self,
                 graph,
                 adj_transform="normalize_adj",
                 attr_transform=None,
                 graph_transform=None,
                 device="cpu",
                 seed=None,
                 name=None,
                 **kwargs):
        r"""Create an optimization - based Batch Virtual Adversarial Training
        Graph Convolutional Networks(OBVAT) model.

        This can be instantiated in the following way:

            model = OBVAT(graph)
                with a `graphgallery.data.Graph` instance representing
                A sparse, attributed, labeled graph.


        Parameters:
        ----------
        graph: An instance of `graphgallery.data.Graph` or a tuple(list) of inputs.
            A sparse, attributed, labeled graph.
        adj_transform: string, `transform`, or None. optional
            How to transform the adjacency matrix. See `graphgallery.functional`
            (default: : obj: `'normalize_adj'` with normalize rate `- 0.5`.
            i.e., math:: \hat{A} = D^{-\frac{1}{2}} A D^{-\frac{1}{2}})
        attr_transform: string, `transform`, or None. optional
            How to transform the node attribute matrix. See `graphgallery.functional`
            (default: obj: `None`)
        device: string. optional
            The device where the model is running on. You can specified `CPU` or `GPU`
            for the model. (default:: str: `CPU: 0`, i.e., running on the `CPU`)
        seed: interger scalar. optional
            Used in combination with `tf.random.set_seed` & `np.random.seed`
            & `random.seed` to create a reproducible sequence of tensors across
            multiple calls. (default: obj: `None`, i.e., using random seed)
        name: string. optional
            Specified name for the model. (default: : str: `class.__name__`)
        kwargs: other custom keyword parameters.
        """
        super().__init__(graph, device=device, seed=seed, name=name,
                         adj_transform=adj_transform,
                         attr_transform=attr_transform,
                         graph_transform=graph_transform,
                         **kwargs)

        self.process()

    def process_step(self):
        graph = self.transform.graph_transform(self.graph)
        adj_matrix = self.transform.adj_transform(graph.adj_matrix)
        node_attr = self.transform.attr_transform(graph.node_attr)

        X, A = gf.astensors(node_attr, adj_matrix, device=self.device)

        # ``A`` and ``X`` are cached for later use
        self.register_cache("X", X)
        self.register_cache("A", A)

    # use decorator to make sure all list arguments have the same length
    @gf.equal()
    def build(self,
              hiddens=[16],
              activations=['relu'],
              dropout=0.5,
              weight_decay=5e-4,
              use_bias=False,
              lr=0.01,
              p1=1.4,
              p2=0.7):

        if self.backend == "torch":
            raise RuntimeError(
                f"Currently {self.name} only supports for tensorflow backend.")

        with tf.device(self.device):

            x = Input(batch_shape=[None, self.graph.num_node_attrs],
                      dtype=self.floatx,
                      name='node_attr')
            adj = Input(batch_shape=[None, None],
                        dtype=self.floatx,
                        sparse=True,
                        name='adj_matrix')
            index = Input(batch_shape=[None],
                          dtype=self.intx,
                          name='node_index')

            GCN_layers = []
            for hidden, activation in zip(hiddens, activations):
                GCN_layers.append(
                    GraphConvolution(
                        hidden,
                        activation=activation,
                        use_bias=use_bias,
                        kernel_regularizer=regularizers.l2(weight_decay)))

            GCN_layers.append(
                GraphConvolution(self.graph.num_node_classes,
                                 use_bias=use_bias))
            self.GCN_layers = GCN_layers
            self.dropout = Dropout(rate=dropout)

            logit = self.forward(x, adj)
            output = Gather()([logit, index])

            model = TFKeras(inputs=[x, adj, index], outputs=output)
            model.compile(loss=SparseCategoricalCrossentropy(from_logits=True),
                          optimizer=Adam(lr=lr),
                          metrics=['accuracy'])

            self.r_vadv = tf.Variable(TruncatedNormal(stddev=0.01)(
                shape=[self.graph.num_nodes, self.graph.num_node_attrs]),
                name="r_vadv")
            entropy_loss = entropy_y_x(logit)
            vat_loss = self.virtual_adversarial_loss(x, adj, logit)
            model.add_loss(p1 * vat_loss + p2 * entropy_loss)

            self.model = model
            self.adv_optimizer = Adam(lr=lr / 10)

    def virtual_adversarial_loss(self, x, adj, logit):

        adv_x = x + self.r_vadv
        logit_p = tf.stop_gradient(logit)
        logit_m = self.forward(adv_x, adj)
        loss = kl_divergence_with_logit(logit_p, logit_m)
        return loss

    def forward(self, x, adj):
        h = x
        for layer in self.GCN_layers:
            h = self.dropout(h)
            h = layer([h, adj])
        return h

    @tf.function
    def extra_train(self, epochs=10):

        with tf.device(self.device):
            r_vadv = self.r_vadv
            optimizer = self.adv_optimizer
            x, adj = self.cache.X, self.cache.A
            r_vadv.assign(TruncatedNormal(stddev=0.01)(shape=tf.shape(r_vadv)))
            for _ in range(epochs):
                with tf.GradientTape() as tape:
                    rnorm = tf.nn.l2_loss(r_vadv)
                    logit = self.forward(x, adj)
                    vloss = self.virtual_adversarial_loss(x, adj, logit)
                    loss = rnorm - vloss
                gradient = tape.gradient(loss, r_vadv)
                optimizer.apply_gradients(zip([gradient], [r_vadv]))

    def train_step(self, sequence):
        self.extra_train()
        return super().train_step(sequence)

    def train_sequence(self, index):

        labels = self.graph.node_label[index]
        sequence = FullBatchSequence(
            [self.cache.X, self.cache.A, index],
            labels,
            device=self.device)
        return sequence
