import tensorflow as tf

from graphgallery.gallery import GalleryModel
from graphgallery.sequence import FullBatchSequence

from graphgallery.nn.models.tensorflow import GCNA as tfGCNA
from graphgallery import functional as gf
from ..gcn import GCN


class GCNA(GCN):
    """
    GCN + node attribute matrix

    Implementation of Graph Convolutional Networks(GCN) concated with node attribute matrix.
    `Semi - Supervised Classification with Graph Convolutional Networks 
    <https://arxiv.org/abs/1609.02907>`
    GCN Tensorflow 1.x implementation: <https://github.com/tkipf/gcn>
    GCN Pytorch implementation: <https://github.com/tkipf/pygcn>

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
        r"""Create a Graph Convolutional Networks(GCN) model 
            concated with node attribute matrix (GCNA).

        This can be instantiated in the following way:

            model = GCNA(graph)
                with a `graphgallery.data.Graph` instance representing
                A sparse, attributed, labeled graph.

        Parameters:
        ----------
        graph: An instance of `graphgallery.data.Graph` or a tuple(list) of inputs.
            A sparse, attributed, labeled graph.
        adj_transform: string, `transform`, or None. optional
            How to transform the adjacency matrix. See `graphgallery.functional`
            (default:: obj: `'normalize_adj'` with normalize rate `- 0.5`.
            i.e., math: : \hat{A} = D^{-\frac{1}{2}} A D^{-\frac{1}{2}})
        attr_transform: string, `transform`, or None. optional
            How to transform the node attribute matrix. See `graphgallery.functional`
            (default: obj: `None`)
        device: string. optional
            The device where the model is running on. You can specified `CPU` or `GPU`
            for the model. (default: : str: `CPU: 0`, i.e., running on the `CPU`)
        seed: interger scalar. optional
            Used in combination with `tf.random.set_seed` & `np.random.seed`
            & `random.seed` to create a reproducible sequence of tensors across
            multiple calls. (default: obj: `None`, i.e., using random seed)
        name: string. optional
            Specified name for the model. (default:: str: `class.__name__`)
        kwargs: other custom keyword parameters.
        """
        super().__init__(graph, device=device, seed=seed, name=name,
                         adj_transform=adj_transform,
                         attr_transform=attr_transform,
                         graph_transform=graph_transform,
                         **kwargs)

    # use decorator to make sure all list arguments have the same length
    @gf.equal()
    def build(self,
              hiddens=[16],
              activations=['relu'],
              dropout=0.5,
              weight_decay=5e-4,
              lr=0.01,
              use_bias=False):

        with tf.device(self.device):
            self.model = tfGCNA(self.graph.num_node_attrs,
                                self.graph.num_node_classes,
                                hiddens=hiddens,
                                activations=activations,
                                dropout=dropout,
                                weight_decay=weight_decay,
                                lr=lr,
                                use_bias=use_bias)
