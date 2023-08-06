import numpy as np
import tensorflow as tf

from graphgallery.gallery import GalleryModel
from graphgallery.sequence import SAGEMiniBatchSequence

from graphgallery.nn.models.tensorflow import GraphSAGE as tfGraphSAGE

from graphgallery import functional as gf


class GraphSAGE(GalleryModel):
    """
        Implementation of SAmple and aggreGatE Graph Convolutional Networks (GraphSAGE). 
        `Inductive Representation Learning on Large Graphs <https://arxiv.org/abs/1706.02216>`
        Tensorflow 1.x implementation: <https://github.com/williamleif/GraphSAGE>
        Pytorch implementation: <https://github.com/williamleif/graphsage-simple/>
    """

    def __init__(self,
                 graph,
                 n_samples=(15, 5),
                 adj_transform="neighbor_sampler",
                 attr_transform=None,
                 graph_transform=None,
                 device="cpu",
                 seed=None,
                 name=None,
                 **kwargs):
        r"""Create a SAmple and aggreGatE Graph Convolutional Networks (GraphSAGE) model.

        This can be instantiated in the following way:

            model = GraphSAGE(graph)
                with a `graphgallery.data.Graph` instance representing
                A sparse, attributed, labeled graph.

        Parameters:
        ----------
        graph: An instance of `graphgallery.data.Graph`.
            A sparse, attributed, labeled graph.
        n_samples: List of positive integer. optional
            The number of sampled neighbors for each nodes in each layer. 
            (default :obj: `(15, 5)`, i.e., sample `15` first-order neighbors and 
            `5` sencond-order neighbors, and the radius for `GraphSAGE` is `2`)
        adj_transform: string, `transform`, or None. optional
            How to transform the adjacency matrix. See `graphgallery.functional`
            (default: :obj:`'neighbor_sampler'`) 
        attr_transform: string, `transform`, or None. optional
            How to transform the node attribute matrix. See `graphgallery.functional`
            (default :obj: `None`)
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

        self.register_cache("n_samples", n_samples)
        self.process()

    def process_step(self):
        graph = self.transform.graph_transform(self.graph)
        # Dense matrix, shape [num_nodes, max_degree]
        adj_matrix = self.transform.adj_transform(graph.adj_matrix)
        node_attr = self.transform.attr_transform(graph.node_attr)
        # pad with a dummy zero vector
        node_attr = np.vstack([node_attr, np.zeros(node_attr.shape[1],
                                                   dtype=self.floatx)])

        X, A = gf.astensor(node_attr, device=self.device), adj_matrix

        # ``A`` and ``X`` are cached for later use
        self.register_cache("X", X)
        self.register_cache("A", A)

    # use decorator to make sure all list arguments have the same length
    @gf.equal()
    def build(self,
              hiddens=[32],
              activations=['relu'],
              dropout=0.5,
              weight_decay=5e-4,
              lr=0.01,
              use_bias=True,
              output_normalize=False,
              aggregator='mean'):

        if self.backend == "tensorflow":
            with tf.device(self.device):
                self.model = tfGraphSAGE(self.graph.num_node_attrs,
                                         self.graph.num_node_classes,
                                         hiddens=hiddens,
                                         activations=activations,
                                         dropout=dropout,
                                         weight_decay=weight_decay,
                                         lr=lr,
                                         use_bias=use_bias,
                                         aggregator=aggregator,
                                         output_normalize=output_normalize,
                                         n_samples=self.cache.n_samples)
        else:
            raise NotImplementedError

    def train_sequence(self, index):

        labels = self.graph.node_label[index]
        sequence = SAGEMiniBatchSequence(
            [self.cache.X, self.cache.A, index],
            labels,
            n_samples=self.cache.n_samples,
            device=self.device)
        return sequence
