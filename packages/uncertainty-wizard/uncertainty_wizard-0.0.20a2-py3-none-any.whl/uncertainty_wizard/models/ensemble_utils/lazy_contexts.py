import abc
import os

import tensorflow as tf


class EnsembleContextManager(abc.ABC):
    """
    An abstract superclass of context managers which can be used to instantiate a context
    on a newly created process.
    """

    def __init__(self, ensemble_id: int, varargs: dict = None):
        self.ensemble_id = ensemble_id,
        self.varargs = varargs

    @abc.abstractmethod
    def __enter__(self) -> None:
        """
        Will be executed before session the model is executed
        :return: None
        """
        pass

    @abc.abstractmethod
    def __exit__(self, type, value, traceback) -> None:
        """
        Will be executed before session the model was executed. You can use this for clean up tasks.
        :return: None
        """
        pass


class NoneContextManager(EnsembleContextManager):
    """
    This context manager makes nothing at all,
    i.e., the model will be executed in exactly the state the process was created.

    This for example implies that the tensorflow default GPU configuration will be used.

    It is save to use this ContextManager on an existing processes where there is already a tf.session
    available.
    """

    def __enter__(self) -> 'NoneContextManager':
        # Docs inherited

        # NoneContext does nothing
        return self

    def __exit__(self, type, value, traceback) -> None:
        # Docs inherited

        # NoneContext does nothing
        pass


class DynamicGpuGrowthContextManager(EnsembleContextManager):
    """
    This context manager configures tensorflow such that multiple processes can use the GPU at the same time.
    It is the default in a lazy ensemble multiprocessing environment
    """

    def __enter__(self) -> 'DynamicGpuGrowthContextManager':
        # Docs inherited
        self.enable_dynamic_gpu_growth()
        return self

    @classmethod
    def enable_dynamic_gpu_growth(cls):
        """
        Configures tensorflow to set memory growth to ture on all GPUs
        :return: None
        """
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

    def __exit__(self, type, value, traceback) -> None:
        # Docs inherited
        pass
