"""Provide random forest machine learning modules
See https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.ranger.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule


class RandomForest(MLProcess):
    """Random Forest model"""
    name = 'MLRandomForest'
    args = MLProcess.args.copy()

class MachineLearningRandomForest(MachineLearningModule):
    """Machine Learning module using random forest"""
    name = 'random-forest'
    long = 'Random Forest'
    model = 'classif.ranger'
    process = RandomForest

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)

ml_modules.register(MachineLearningRandomForest())
