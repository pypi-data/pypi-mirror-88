import random
import torch
import os
import sys
import uuid

import numpy as np
import tensorflow as tf
import os.path as osp
import scipy.sparse as sp

from tensorflow.keras import backend as K

import graphgallery as gg
from graphgallery.data.io import makedirs_from_filepath
from graphgallery.utils import saver
from graphgallery import functional as gf

from .model import Model


def cache_transform(transform_kwargs):
    graph_transform = gf.get(transform_kwargs.pop("graph_transform", None))
    adj_transform = gf.get(transform_kwargs.pop("adj_transform", None))
    attr_transform = gf.get(transform_kwargs.pop("attr_transform", None))
    label_transform = gf.get(transform_kwargs.pop("label_transform", None))

    return gf.BunchDict(graph_transform=graph_transform,
                        adj_transform=adj_transform,
                        attr_transform=attr_transform,
                        label_transform=label_transform)


class GraphModel(Model):
    """Base model for Graph Neural Network (GNNs)."""

    def __init__(self, graph, device="cpu", seed=None, name=None, **kwargs):
        r"""Create a base model for Graph Neural Network (GNNs).

        Parameters:
        ----------
        graph: Graph or MultiGraph.
        device: string. optional
            The device where the model running on.
        seed: interger scalar. optional
            Used in combination with `tf.random.set_seed` & `np.random.seed`
            & `random.seed` to create a reproducible sequence of tensors
            across multiple calls.
        name: string. optional
            Specified name for the model. (default: :str: `class.__name__`)
        kwargs: keyword parameters for transform, including:
            ``adj_transform``, ``attr_transform``, 
            ``label_transform``, ``graph_transform``, etc.

        """
        self.transform = cache_transform(kwargs)
        super().__init__(graph, device=device, seed=seed, name=name, **kwargs)

        self.train_data = None
        self.val_data = None
        self.test_data = None
        self.predict_data = None
        self.backup = None

        self._model = None
        self._custom_objects = None  # used for save/load TF model

        # checkpoint path
        # use `uuid` to avoid duplication
        self.ckpt_path = osp.join(os.getcwd(), f"{self.name}_checkpoint_{uuid.uuid1().hex[:6]}{gg.file_ext()}")

    def save(self,
             path=None,
             as_model=False,
             overwrite=True,
             save_format=None,
             **kwargs):

        if not path:
            path = self.ckpt_path

        makedirs_from_filepath(path)

        if as_model:
            if self.backend == "tensorflow":
                saver.save_tf_model(self.model,
                                    path,
                                    overwrite=overwrite,
                                    save_format=save_format,
                                    **kwargs)
            else:
                saver.save_torch_model(self.model,
                                       path,
                                       overwrite=overwrite,
                                       save_format=save_format,
                                       **kwargs)
        else:
            if self.backend == "tensorflow":
                saver.save_tf_weights(self.model,
                                      path,
                                      overwrite=overwrite,
                                      save_format=save_format)
            else:
                saver.save_torch_weights(self.model,
                                         path,
                                         overwrite=overwrite,
                                         save_format=save_format)

    def load(self, path=None, as_model=False):
        if not path:
            path = self.ckpt_path

        # if not osp.exists(path):
        #     print(f"{path} do not exists.", file=sys.stderr)
        #     return

        if as_model:
            if self.backend == "tensorflow":
                self.model = saver.load_tf_model(
                    path, custom_objects=self.custom_objects)
            else:
                self.model = saver.load_torch_model(path)
        else:
            if self.backend == "tensorflow":
                saver.load_tf_weights(self.model, path)
            else:
                saver.load_torch_weights(self.model, path)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, m):
        # Back up
        if isinstance(m, tf.keras.Model) and m.weights:
            self.backup = tf.identity_n(m.weights)
        # TODO assert m is None or isinstance(m, tf.keras.Model) or torch.nn.Module
        self._model = m

    @property
    def custom_objects(self):
        return self._custom_objects

    @custom_objects.setter
    def custom_objects(self, objs):
        assert isinstance(objs, dict), objs
        self._custom_objects = objs

    def close(self):
        """Close the session of model and empty cache."""
        gg.empty_cache()
        self._model = None

    def __call__(self, *args, **kwargs):
        return self._model(*args, **kwargs)
