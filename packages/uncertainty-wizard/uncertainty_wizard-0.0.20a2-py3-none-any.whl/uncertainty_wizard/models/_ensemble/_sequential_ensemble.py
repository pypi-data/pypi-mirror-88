from typing import List

import tensorflow as tf

from uncertainty_wizard.models._ensemble._abstract_ensemble import Ensemble


class EnsembleSequential(Ensemble):

    def __init__(self, layers=None, num_models=32,
                 models: List[tf.keras.Sequential] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert models is None or layers is None, \
            "If models are already provided, the other inputs are ignored. " \
            "Thus, the first positional arg (layers) must be None"
        if models is None:
            self._inners = [tf.keras.models.Sequential() for _ in range(num_models)]
            if layers is not None:
                for layer in layers:
                    self.add(layer)
            # Note on Else: Base-Layer default initializer is tf.keras.initializers.glorot_uniform,
            # which works fine for us. If someone wants to change this, the simplest
            # version is to do it outside of uwiz and to pass the models with custom config trhough the models param
        else:
            # Shallow Copy
            self._inners = [m for m in models]

    @property
    def inner(self) -> List[tf.keras.Model]:
        return self._inners

    def add(self, layer):
        """
        Adds the passed layer to every model in the ensemble.
        Note that different instances of the layer should be created for every model in the ensemble.

        Thus, the passed layer is expected to be in one of the following forms:

        - A no-args lambda or function, returning a layer instance on every call

        - A layer instance which can be copied using get_config and from_config

        Note that if passing a layer directly instead of a lambda,
        the layer is copied through `get_config` and `from_config`.
        Properties which are not specified in the layers config are thus not used in the ensembles models layers.

        Args:
            layer: a no-args layer creating function or lambda. One instance of the created layer will be added to every model in the ensemble

        Returns:
            None
        """
        # Old Input Layers are tensors. We map them to layer instances.
        if hasattr(layer, '_keras_history'):
            origin_layer = layer._keras_history[0]
            if isinstance(origin_layer, tf.keras.layers.InputLayer):
                layer = origin_layer

        # Create layer factories based on the provided layer
        if isinstance(layer, tf.keras.layers.Layer):
            layer_supplier = lambda: type(layer).from_config(layer.get_config())
        else:
            layer_supplier = layer
        for model in self._inners:
            new_layer = layer_supplier()
            assert isinstance(layer, tf.keras.layers.Layer), \
                "the layer parameter must be either a no-args function which returns a `tf.keras.layers.Layer`" \
                "or a `tf.keras.layers.Layer`"
            model.add(new_layer)
