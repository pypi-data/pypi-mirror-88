"""Provide glmnet machine learning modules
See https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.glmnet.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule


class MLGlmnet(MLProcess):
    """Penalized Logistic Regression model"""
    name = 'MLGlmnet'
    args = MLProcess.args.copy()

class MachineLearningGlmnet(MachineLearningModule):
    """Machine Learning module using Penalized Logistic Regression"""
    name = 'glmnet'
    long = 'Penalized Logistic Regression'
    model = 'classif.glmnet'
    process = MLGlmnet

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        self.process.args['factorize_chars'] = True

ml_modules.register(MachineLearningGlmnet())
