from typing import List

import tensorflow as tf

from uncertainty_wizard.models.ensemble.abstract_ensemble import AbstractEnsemble


class EnsembleFunctional(AbstractEnsemble):

    def __init__(self, inputs, outputs,
                 num_models=32,
                 clone_function=lambda layer: layer.__class__.from_config(layer.get_config()),
                 clone_weights: bool = False,
                 models: List[tf.keras.Model] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert models is None or (inputs is None and outputs is None), \
            "If models are already provided, the other inputs are ignored. " \
            "To prevent misconceptions, the first two positional args (inputs & outputs) must be set to None"
        if models is None:
            base_model = tf.keras.Model(inputs, outputs)
            self._inners = [tf.keras.models.clone_model(model=base_model,
                                                        clone_function=clone_function) for _ in range(num_models)]
            if clone_weights:
                weights = base_model.get_weights()
                for model in self._inners:
                    model.set_weights(weights)
            # Note on Else: Base-Layer default initializer is tf.keras.initializers.glorot_uniform,
            # which works fine for us. If someone wants to change this, the simplest
            # version is to do it outside of uwiz and to pass the models with custom config trhough the models param
        else:
            # Shallow copy
            self._inners = [m for m in models]



    @property
    def _inner(self) -> List[tf.keras.Model]:
        return self._inners
