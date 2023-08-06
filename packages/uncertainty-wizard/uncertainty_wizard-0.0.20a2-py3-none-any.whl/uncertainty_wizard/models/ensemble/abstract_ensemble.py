import abc
import logging
import os
import pickle
import shutil
import warnings
from typing import List, Union, Iterable, Any

import numpy as np
import tensorflow as tf

from uncertainty_wizard.models import warn_utils
from uncertainty_wizard.models._uwiz_model import _UwizModel
from uncertainty_wizard.quantifiers import Quantifier


def preprocess_path(path: str) -> str:
    """
    Preprocesses the path, i.e.,
    (1) Converts potential file paths into folder paths. Endings (e.g. h5 are ignored)
    (2) Makes sure there's no tailing '/' or '\'
    :param path: The path as passed by the user
    :return: The path of the folder on which the model will be stored
    """
    root, ext = os.path.splitext(path)
    if not ext == "":
        warnings.warn(
            f"{path} is the path for a file, but to save ensembles, you need to pass the path of a folder."
            f"We will use {root} instead"
        )
        path = root

    if path.endswith("/") or path.endswith("\\"):
        path = path[:len(path) - 1]

    return path


def config_file_path(path):
    # This will be a repeated preprocessing in most cases,
    #   but we do it every time nonetheless, to avoid nasty bugs due to forgotten preprocessing
    path = preprocess_path(path)
    return f'{path}/save_config.pickle'


class AbstractEnsemble(_UwizModel):

    @property
    @abc.abstractmethod
    def _inner(self) -> List[tf.keras.Model]:
        pass  # pragma: no cover

    @property
    def _call_forker(self) -> 'CallForker':
        # Note, we recompute this every time a CallForker is needed.
        # We could in theory cache it, but the call is very fast and if something
        # else changes the available methods on the wrapped models or the list of wrapped models,
        # a new CallForker take these changes into account
        return CallForker(wrapped=self._inner)

    @property
    def compile(self):
        """
        Direct access to the fit methods the wrapped keras models.
        See `tf.keras.Model.compile` for precise documentation of this method.

        Can be called as `model.compile(...)`, equivalent to how compile would be called on a plain keras model.
        :return: The compile method of the wrapped model
        """
        # Reason for disabled linting: CallForker methods are added at runtime and not visible for static code analysis
        # noinspection PyUnresolvedReferences
        return self._call_forker.compile  # pylint: disable=no-member

    @property
    def fit(self):
        """
        Direct access to the fit methods the wrapped keras models.
        See `tf.keras.Model.fit` for precise documentation of this method.

        Can be called as `model.fit(...)`, equivalent to how fit would be called on a plain keras model.
        :return: The fit method of the wrapped model
        """
        # Reason for disabled linting: CallForker methods are added at runtime and not visible for static code analysis
        # noinspection PyUnresolvedReferences
        return self._call_forker.fit  # pylint: disable=no-member

    def predict_quantified(self, x: np.ndarray,
                           quantifier: Union[Quantifier, Iterable[Quantifier]],
                           # Other Sequential.predict params (e.g. Callbacks) are not yet supported
                           batch_size: int = 32,
                           verbose: int = 0,
                           steps=None,
                           as_confidence: Union[None, bool] = None,
                           blindly_trust_input: bool = False):
        if not isinstance(x, np.ndarray):
            if blindly_trust_input:
                logging.warning("Blindly trusting the passed non-numpy input")
            else:
                raise TypeError("In ensemble models, the most efficient implementation "
                                "(in which we execute the models sequentially)"
                                "requires to iterate over the passed data once per model."
                                "As tf.data.Datasets and generators may provide different inputs "
                                "on every iteration, they are officially not supported in uwiz ensembles."
                                "\n"
                                "If you are absolutely sure that your input provides the same values on every"
                                "iteration, you can pass the flag `blindly_trust_input` to predict_quantified"
                                "on ensembles.")

        all_q, pp_q, sample_q, return_single_tuple = self._quantifiers_as_list(quantifier)
        warn_utils.check_quantifier_heterogenity(as_confidence=as_confidence, quantifiers=all_q)

        if len(pp_q) > 0:
            raise ValueError("Point predictor quantifiers are not supported in ensemble models:"
                             f"{','.join([type(q) for q in pp_q])}")

        # Note: it would be quite easy to pack all models in one graph instance:
        #   While more easily generalizable w.r.t. different input structures,
        #   the graph would quickly become too large in real-sized ensembles.
        #   Thus, we chose an iterative procedure
        # noinspection PyUnresolvedReferences
        predictions_by_model = self._call_forker.predict(x, batch_size=batch_size, verbose=verbose,
                                                         steps=steps)  # pylint: disable=no-member
        scores = None
        for i, predictions in enumerate(predictions_by_model):
            if scores is None:
                scores_shape = list(predictions.shape)
                scores_shape.insert(1, len(self._inner))
                scores = np.empty(scores_shape)
            scores[:, i] = predictions

        results = []
        for q in all_q:
            predictions, superv_scores = q.calculate(scores)
            superv_scores = q.cast_conf_or_unc(as_confidence=as_confidence, superv_scores=superv_scores)
            results.append((predictions, superv_scores))
        if return_single_tuple:
            return results[0]
        return results

    def save(self, path: str,
             overwrite=True,
             include_optimizer=True,
             save_format: Any = None,
             signatures: Any = None,
             options: Any = None):
        """
        Similarly to `tf.keras.models.save_model`, this method saves the ensemble to the file system.

        There are 2 notable differences:

        - The provided path must be a path to a folder
        - If 'include_optimizer' is false, this will save the architecture and weights of the first model
          in the ensemble and just the weights for all remaining models.
          During deserialization, the architecture of the first model will be used
          for all models in the ensemble.

        :param path: Must be a folder
        :param overwrite: See `tf.keras.models.save_model` documentation
        :param include_optimizer: Boolean on whether to use the efficient save configuration explained above.
        :param save_format: See `tf.keras.models.save_model` documentation
        :param signatures: See `tf.keras.models.save_model` documentation
        :param options: See `tf.keras.models.save_model` documentation
        """

        path = preprocess_path(path=path)
        self._create_or_empty_folder(path=path, overwrite=overwrite)

        save_config = {
            "num_models": len(self._inner),
            "include_optimizer": include_optimizer
        }
        with open(config_file_path(path), 'wb') as f:
            pickle.dump(save_config, f)

        if include_optimizer:
            logging.warning("You are saving an ensemble models including optimizers."
                            "We will write all the models of the ensemble completely to the file, which "
                            "can take a large amount of space."
                            "If you are not planning to continue training, set `include_optimizer` to false"
                            "In that case, we will much more efficiently save the architecture of the first model"
                            "and and just the weights for all remaining models.")
            self._save_complete(include_optimizer, options, path, save_format, signatures)
        else:
            self._save_efficiently(include_optimizer, options, path, save_format, signatures)

    def _save_efficiently(self, include_optimizer, options, path, save_format, signatures):
        for i, model in enumerate(self._inner):
            model_path = f"{path}/inner_model_{i}"
            if i == 0:
                tf.keras.models.save_model(model,
                                           filepath=model_path,
                                           # We're working in an empty folder (overwrite was checked before)
                                           overwrite=False,
                                           include_optimizer=include_optimizer,
                                           save_format=save_format,
                                           signatures=signatures,
                                           options=options)
            else:
                model.save_weights(filepath=model_path,
                                   # We're working in an empty folder (overwrite was checked before)
                                   overwrite=False,
                                   save_format=save_format,
                                   options=options)

    def _save_complete(self, include_optimizer, options, path, save_format, signatures):
        for i, model in enumerate(self._inner):
            model_path = f"{path}/inner_model_{i}"
            tf.keras.models.save_model(model,
                                       filepath=model_path,
                                       # We're working in an empty folder (see above)
                                       overwrite=False,
                                       include_optimizer=include_optimizer,
                                       save_format=save_format,
                                       signatures=signatures,
                                       options=options)

    @staticmethod
    def _create_or_empty_folder(path: str, overwrite: bool) -> None:
        if os.path.exists(path=path):
            if overwrite:
                shutil.rmtree(path, ignore_errors=False, onerror=None)
                os.mkdir(path)
            else:
                raise ValueError(f"Save folder {path} already exists and you specified `overwrite=False`. ")
        else:
            os.makedirs(path)


class CallForker:

    def __init__(self, wrapped: List):
        assert len(wrapped) > 0, "must wrap at least one model"
        method_list = [func for func in dir(wrapped[0]) if not func.startswith('_')]
        for method in method_list:
            def make_function(inner_method=method):
                def call_on_all(*args, **kwargs):
                    res = []
                    for model in wrapped:
                        this_model_res = getattr(model, inner_method)(*args, **kwargs)
                        res.append(this_model_res)
                    return res

                return call_on_all

            setattr(self, method, make_function())
