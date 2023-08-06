import tensorflow as tf

from uncertainty_wizard.models.stochastic.abstract_stochastic import _AbstractStochastic
from uncertainty_wizard.models.stochastic.stochastic_mode import StochasticMode


class StochasticFunctional(_AbstractStochastic):

    def __init__(self, inputs, outputs, stochastic_mode: StochasticMode, name: str = None):
        super().__init__()
        self._inner_model = tf.keras.Model(inputs=inputs, outputs=outputs, name=name)
        self._inner_model._stochastic_mode_tensor = stochastic_mode.as_tensor()

    @property
    def _inner(self):
        return self._inner_model

    @property
    def _stochastic_mode_tensor(self):
        return self._inner_model._stochastic_mode_tensor

    @classmethod
    def _wrap(cls, inner: tf.keras.Model, stochastic_mode_tensor=None):
        if stochastic_mode_tensor is None:
            assert inner._stochastic_mode_tensor is not None, \
                "Uncertainty Wizard internal error. " \
                "Trying to wrap a model that has no stochastic_mode_tensor, " \
                "and no external stochastic_mode_tensor is passed to attach"
            stochastic_mode_tensor = inner._stochastic_mode_tensor
        stochastic_mode = StochasticMode(stochastic_mode_tensor)
        return StochasticFunctional(inner.inputs, inner.outputs, stochastic_mode=stochastic_mode)
