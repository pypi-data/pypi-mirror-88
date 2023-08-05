"""Gradient Boosting machine learning modules
See
https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.xgboost.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule

class MLXgboost(MLProcess):
    """Gradient Boosting"""
    name = 'MLXgboost'
    args = MLProcess.args.copy()

class MachineLearningXgboost(MachineLearningModule):
    """Machine Learning module using Gradient Boosting"""
    name = 'xgboost'
    long = 'Gradient Boosting'
    model = 'classif.xgboost'
    process = MLXgboost

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        self.process.args['factorize_chars'] = True

ml_modules.register(MachineLearningXgboost())
