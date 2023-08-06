from tensorflow.keras import Input
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.losses import SparseCategoricalCrossentropy

from graphgallery.nn.layers.tensorflow import ChebyConvolution, Gather
from graphgallery import floatx, intx
from graphgallery.nn.models import TFKeras


class ChebyNet(TFKeras):

    def __init__(self, in_channels, out_channels,
                 hiddens=[16],
                 activations=['relu'],
                 dropout=0.5,
                 weight_decay=5e-4,
                 lr=0.01, order=2, use_bias=False):

        x = Input(batch_shape=[None, in_channels],
                  dtype=floatx(), name='node_attr')
        adj = [Input(batch_shape=[None, None],
                     dtype=floatx(), sparse=True,
                     name=f'adj_matrix_{i}') for i in range(order + 1)]
        index = Input(batch_shape=[None], dtype=intx(), name='node_index')

        h = x
        for hidden, activation in zip(hiddens, activations):
            h = ChebyConvolution(hidden, order=order, use_bias=use_bias,
                                 activation=activation,
                                 kernel_regularizer=regularizers.l2(weight_decay))([h, adj])
            h = Dropout(rate=dropout)(h)

        h = ChebyConvolution(out_channels,
                             order=order, use_bias=use_bias)([h, adj])
        h = Gather()([h, index])

        super().__init__(inputs=[x, *adj, index], outputs=h)
        self.compile(loss=SparseCategoricalCrossentropy(from_logits=True),
                     optimizer=Adam(lr=lr), metrics=['accuracy'])
