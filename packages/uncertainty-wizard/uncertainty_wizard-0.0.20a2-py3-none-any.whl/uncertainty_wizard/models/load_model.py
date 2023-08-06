import os
import pickle
from typing import Any, List

import tensorflow as tf

import uncertainty_wizard as uwiz
from uncertainty_wizard.models.ensemble.abstract_ensemble import AbstractEnsemble
from uncertainty_wizard.models import StochasticSequential, StochasticFunctional, EnsembleSequential, EnsembleFunctional


def load_model(path, custom_objects: dict = None, compile=True, options=None):
    """
    Loads an uncertainty wizard model that was saved using model.save(...).
    See the documentation of `tf.keras.models.load_model` for further information about the method params.

    For ensembles: The passed parameters are passed to the deserialization of every of the individual wrapped models.

    Args:
        path (): The path of the folder where the ensemble was saved.
        custom_objects (): Dict containing methods for custom deserialization of objects.
        compile (): Whether to compile the models.
        options (): Load options, check tf.keras documentation for precise information.

    Returns:
        An uwiz model.
    """
    # Note: a path without file extension is not necessarily an ensemble in a folder
    # It could be a user who stored a stochastic model with default (non specified) file ending
    # Thus, we have to check if the folder exists and contains an ensemble config file
    ensemble_config_path = uwiz.models.ensemble.abstract_ensemble.config_file_path(path)
    if os.path.isdir(path) and os.path.exists(path) and os.path.exists(ensemble_config_path):
        return _load_ensemble(path=path,
                              custom_objects=custom_objects,
                              compile=compile, options=options)
    else:
        return _load_stochastic(path=path,
                                custom_objects=custom_objects,
                                compile=compile, options=options)


def _load_stochastic(path, custom_objects: dict = None, compile=None, options=None):
    # Note: We currently intentionally don't define stochastic layers as custom_objects
    # as they have no methods other than call that we rely on, and thus the (robust and easy to maintain)
    # tf deserialization is sufficient

    inner = tf.keras.models.load_model(path, custom_objects=custom_objects, compile=compile, options=options)
    assert hasattr(inner, '_stochastic_mode_tensor'), \
        "Looks like the model which is being deserialized is not an uwiz stochastic model"

    if isinstance(inner, tf.keras.models.Sequential):
        return StochasticSequential._wrap(inner)
    else:
        return StochasticFunctional._wrap(inner)


def _load_ensemble(path,
                   custom_objects: Any = None,
                   compile: bool = True,
                   options: Any = None):
    path = uwiz.models.ensemble.abstract_ensemble.preprocess_path(path=path)
    with open(uwiz.models.ensemble.abstract_ensemble.config_file_path(path), 'rb') as f:
        save_config = pickle.load(f)
    num_models = save_config["num_models"]
    new_inners = []
    includes_optimizer = bool(save_config["include_optimizer"])
    for i in range(num_models):
        model_path = f"{path}/inner_model_{i}"
        if includes_optimizer or i == 0:
            m = tf.keras.models.load_model(model_path, custom_objects=custom_objects, compile=compile, options=options)
        else:
            # Only weights are stored for all but the first model if includes_optimizer is False
            m = tf.keras.models.clone_model(model=new_inners[0])
            m.load_weights(filepath=model_path)
        new_inners.append(m)

    if isinstance(new_inners[0], tf.keras.models.Sequential):
        return EnsembleSequential(models=new_inners)
    else:
        return EnsembleFunctional(inputs=None, outputs=None, models=new_inners)
