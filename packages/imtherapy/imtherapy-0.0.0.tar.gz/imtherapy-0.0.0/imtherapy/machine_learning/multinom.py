"""Provide Multinomial log-linear model machine learning modules
See
https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.multinom.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule


class MLMultinom(MLProcess):
    """Multinomial log-linear model model"""
    name = 'MLMultinom'
    args = MLProcess.args.copy()

class MachineLearningMultinom(MachineLearningModule):
    """Machine Learning module using Multinomial log-linear model"""
    name = 'multinom'
    long = 'Multinomial log-linear model'
    model = 'classif.multinom'
    process = MLMultinom

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        self.process.args['factorize_chars'] = True

ml_modules.register(MachineLearningMultinom())
