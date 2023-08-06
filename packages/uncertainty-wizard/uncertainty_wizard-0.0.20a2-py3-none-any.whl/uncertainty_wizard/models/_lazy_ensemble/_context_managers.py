import abc
import os
import random
import time

import tensorflow as tf
from tensorflow import Graph


class EnsembleContextManager(abc.ABC):
    def __init__(self, ensemble_id: int, varargs: dict = None):
        self.ensemble_id = ensemble_id,
        self.varargs = varargs

    @abc.abstractmethod
    def __enter__(self) -> None:
        pass

    @abc.abstractmethod
    def __exit__(self, type, value, traceback) -> None:
        pass


class NoneContext(EnsembleContextManager):

    def __enter__(self) -> 'NoneContext':
        # NoneContext does nothing
        return self

    def __exit__(self, type, value, traceback) -> None:
        # NoneContext does nothing
        pass


class DynamicGpuGrowthContextManager(EnsembleContextManager):

    def __enter__(self) -> 'DynamicGpuGrowthContextManager':
        self.enable_dynamic_gpu_growth()
        return self

    @classmethod
    def enable_dynamic_gpu_growth(cls):
        if "CUDA_VISIBLE_DEVICES" in os.environ:
            del os.environ["CUDA_VISIBLE_DEVICES"]
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                # Currently, memory growth needs to be the same across GPUs
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                # Memory growth must be set before GPUs have been initialized
                print(e)
        if len(gpus) > 1:
            tf.distribute.experimental_set_strategy(
                tf.distribute.MirroredStrategy()
            )

    def __exit__(self, type, value, traceback) -> None:
        pass
