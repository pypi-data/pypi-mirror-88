"""Provide k-Nearest-Neighbor machine learning modules
See https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.kknn.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule


class MLKknn(MLProcess):
    """k-Nearest Neighbors model"""
    name = 'MLKknn'
    args = MLProcess.args.copy()

class MachineLearningKknn(MachineLearningModule):
    """Machine Learning module using k-Nearest Neighbors"""
    name = 'kknn'
    long = 'k-Nearest Neighbors'
    model = 'classif.kknn'
    process = MLKknn

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        self.process.args['factorize_chars'] = True

ml_modules.register(MachineLearningKknn())
