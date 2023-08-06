from .model import Model
from .graph_model import GraphModel
from .gallery_model.gallery_model import GalleryModel
from .sklearn_model.sklearn_model import SklearnModel

import sys
import importlib
from typing import Tuple
from graphgallery import backend
from graphgallery import functional as gf

__all__ = ["Gallery", "Model"]

Gallery = gf.Registry("GraphGalleryModels")

_GALLERY_MODELS = {
    "GCN",
    "GAT",
    "ClusterGCN",
    "SGC",
    "GWNN",
    "RobustGCN",
    "GraphSAGE",
    "FastGCN",
    "ChebyNet",
    "DenseGCN",
    "LGCN",
    "OBVAT",
    "SBVAT",
    "GMNN",
    "DAGNN",
    # Experimental models
    "EdgeGCN",
    "SimplifiedOBVAT",
    "GCN_MIX",
    "GCNA",
    "SAT",
    "MedianGCN"    
}

_SKLEARN_MODELS = {
    "Node2vec",
    "Deepwalk",
}


def _gen_missing_model(model, backend):
    def _missing_model(*args, **kwargs):
        raise ImportError(f"model {model} is not supported by '{backend}'."
                          " You can switch to other backends by setting"
                          " the 'graphgallery.backend' environment.")

    return _missing_model


def load_models(backend_name=None):
    _backend = backend(backend_name)
    thismod = sys.modules[__name__]
    mod = importlib.import_module(f".gallery_model.{_backend.abbr}", __name__)

    global Gallery
    Gallery = gf.Registry("GraphGalleryModels")

    for model in _GALLERY_MODELS:
        _model_class = mod.__dict__.get(model, None)

        if _model_class is not None:
            Gallery.register(_model_class)
            setattr(thismod, model, _model_class)
        else:
            setattr(thismod, model, _gen_missing_model(model, _backend))

    mod = importlib.import_module(f".sklearn_model", __name__)

    for model in _SKLEARN_MODELS:
        _model_class = mod.__dict__.get(model, None)

        if _model_class is not None:
            Gallery.register(_model_class)
            setattr(thismod, model, _model_class)
        else:
            setattr(thismod, model, _gen_missing_model(model, _backend))


def is_enabled(model: str) -> bool:
    """Return true if the model is enabled by the current backend.

    Parameters
    ----------
    model : str
        The model name.

    Returns
    -------
    bool
        True if the model is enabled by the current backend.
    """
    return model in Gallery


def enabled_models() -> Tuple[str]:
    """Return the models in the gallery enabled by the current backend.

    Returns
    -------
    tuple
        A list of models enabled by the current backend.
    """
    return tuple(Gallery.names())


load_models()
