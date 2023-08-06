from typing import List

import numpy as np

from uncertainty_wizard.quantifiers import predictive_entropy
from uncertainty_wizard.quantifiers.quantifier import UncertaintyQuantifier, ProblemType


def validate_shape(nn_outputs):
    assert len(nn_outputs.shape) >= 2, "nn_outputs for Average Standard Deviation must have shape " \
                                       "(number_of_inputs, num_samples, pred_dim_1, pred_dim_2, ...)"
    num_inputs = nn_outputs.shape[0]
    num_samples = nn_outputs.shape[1]
    return num_inputs, num_samples


class StandardDeviation(UncertaintyQuantifier):

    @classmethod
    def takes_samples(cls) -> bool:
        # Docs inherited
        return True

    @classmethod
    def problem_type(cls) -> ProblemType:
        # Docs inherited
        return ProblemType.REGRESSION

    @classmethod
    def aliases(cls) -> List[str]:
        # Docs inherited
        return ["standard_deviation", "std_dev", "std", "stddev", "StandardDeviation"]

    @classmethod
    def calculate(cls, nn_outputs: np.ndarray):
        # Docs inherited
        _, _ = validate_shape(nn_outputs)
        predictions = np.mean(nn_outputs, axis=1)
        uncertainties = np.std(nn_outputs, axis=1)
        return predictions, uncertainties


class RegressionEntropy(UncertaintyQuantifier):

    @classmethod
    def takes_samples(cls) -> bool:
        # Docs inherited
        return True

    @classmethod
    def problem_type(cls) -> ProblemType:
        # Docs inherited
        return ProblemType.REGRESSION

    @classmethod
    def aliases(cls) -> List[str]:
        # Docs inherited
        return ["regression-entropy", "regression_entropy", "RegressionEntropy", "RE"]

    @classmethod
    def calculate(cls, nn_outputs: np.ndarray):
        # Docs inherited
        _, _ = validate_shape(nn_outputs)
        predictions = np.mean(nn_outputs, axis=1)
        uncertainties = predictive_entropy.entropy(nn_outputs, axis=1)
        return predictions, uncertainties
