"""Provide Linear discriminant analysis machine learning modules
See https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.lda.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule


class MLLda(MLProcess):
    """Linear discriminant analysis model"""
    name = 'MLLda'
    args = MLProcess.args.copy()

class MachineLearningLda(MachineLearningModule):
    """Machine Learning module using k-Nearest Neighbors"""
    name = 'lda'
    long = 'Linear discriminant analysis'
    model = 'classif.lda'
    process = MLLda

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        self.process.args['factorize_chars'] = True

ml_modules.register(MachineLearningLda())
