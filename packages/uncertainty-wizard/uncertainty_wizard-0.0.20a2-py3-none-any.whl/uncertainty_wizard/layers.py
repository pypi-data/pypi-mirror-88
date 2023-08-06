import warnings

import tensorflow as tf
from tensorflow.python.keras.layers import GaussianNoise

from uncertainty_wizard.internal_utils import UncertaintyWizardWarning
from uncertainty_wizard.models._stochastic._stochastic_mode import StochasticMode

_MISSING_STOCHASTIC_MODE_ERROR = "No stochastic mode instance was provided when creating the randomized layer. " \
                                 "A stochastic mode is required to use the randomization for predictions"


def has_casting_preventing_subtype(instance, expected_type, corresponding_uw_type) -> bool:
    i_type = type(instance)
    if issubclass(i_type, expected_type) and not issubclass(expected_type, i_type):
        # The instance is from a (strict) subclass of the expected type
        if isinstance(instance, corresponding_uw_type):
            warnings.warn(f"Looks like you are passing an {corresponding_uw_type} layer."
                          f"For SequentialStochastic layers, it is sufficient to pass a layer of"
                          f"the corresponding keras layer {expected_type}."
                          f"We trust you that you know what you did and set up the stochastic mode correctly."
                          f"Your layer will thus not be replaced, but added to the model as you provided it.",
                          UncertaintyWizardWarning)
        else:
            warnings.warn(f"Looks like you are passing an instance of a custom subtype of {expected_type}."
                          f"We typically replace {expected_type} instances with our own custom subtype."
                          f"We will not do this with your custom subtype instance. "
                          f"If you want to use it for randomness during inference, "
                          f"make sure the models stochastic mode tensor is respected in your layer.",
                          UncertaintyWizardWarning)
        return True
    return False


class UwizBernoulliDropout(tf.keras.layers.Dropout):

    def __init__(self, rate, stochastic_mode: StochasticMode, noise_shape=None, seed=None, **kwargs):
        super().__init__(rate, noise_shape, seed, **kwargs)
        assert stochastic_mode is not None, _MISSING_STOCHASTIC_MODE_ERROR
        self.stochastic_mode = stochastic_mode
        # We must not call super from within tf.cond
        self._super = super()

    def call(self, inputs, training=None):
        return tf.cond(self.stochastic_mode.as_tensor(),
                       lambda: self._super.call(inputs=inputs, training=True),
                       lambda: self._super.call(inputs=inputs, training=training))

    @classmethod
    def from_keras_layer(cls, layer: tf.keras.layers.Dropout, stochastic_mode: StochasticMode):
        if has_casting_preventing_subtype(layer, tf.keras.layers.Dropout, UwizBernoulliDropout):
            return layer
        else:
            rate = layer.rate
            noise_shape = layer.noise_shape
            seed = layer.seed
            return UwizBernoulliDropout(rate=rate, noise_shape=noise_shape, seed=seed, stochastic_mode=stochastic_mode)

    def get_config(self):
        config = super(UwizBernoulliDropout, self).get_config()
        config['name'] = 'UwBernoulliDropout'
        return config


class UwizGaussianDropout(tf.keras.layers.GaussianDropout):

    def __init__(self, rate, stochastic_mode: StochasticMode, **kwargs):
        super().__init__(rate, **kwargs)
        assert stochastic_mode is not None, _MISSING_STOCHASTIC_MODE_ERROR
        self.stochastic_mode = stochastic_mode
        # We must not call super from within tf.cond
        self._super = super()

    def call(self, inputs, training=None):
        return tf.cond(self.stochastic_mode.as_tensor(),
                       lambda: self._super.call(inputs=inputs, training=True),
                       lambda: self._super.call(inputs=inputs, training=training))

    @classmethod
    def from_keras_layer(cls, layer: tf.keras.layers.GaussianDropout, stochastic_mode: StochasticMode):
        if has_casting_preventing_subtype(layer, tf.keras.layers.GaussianDropout, UwizGaussianDropout):
            return layer
        else:
            rate = layer.rate
            return UwizGaussianDropout(rate=rate, stochastic_mode=stochastic_mode)

    def get_config(self):
        config = super(UwizGaussianDropout, self).get_config()
        config['name'] = 'UwGaussianDropout'
        # No custom config yet.
        return config


class UwizGaussianNoise(tf.keras.layers.GaussianNoise):

    def __init__(self, stddev, stochastic_mode: StochasticMode, **kwargs):
        super().__init__(stddev, **kwargs)
        assert stochastic_mode is not None, _MISSING_STOCHASTIC_MODE_ERROR
        self.stochastic_mode = stochastic_mode
        # We must not call super from within tf.cond
        self._super = super()

    def call(self, inputs, training=None):
        return tf.cond(self.stochastic_mode.as_tensor(),
                       lambda: self._super.call(inputs=inputs, training=True),
                       lambda: self._super.call(inputs=inputs, training=training))

    @classmethod
    def from_keras_layer(cls, layer: tf.keras.layers.GaussianNoise, stochastic_mode: StochasticMode):
        if has_casting_preventing_subtype(layer, tf.keras.layers.GaussianNoise, UwizGaussianNoise):
            return layer
        else:
            stddev = layer.stddev
            return UwizGaussianNoise(stddev=stddev, stochastic_mode=stochastic_mode)

    def get_config(self):
        config = super(GaussianNoise, self).get_config()
        config['name'] = 'UwGaussianNoise'
        # No custom config yet.
        return config
