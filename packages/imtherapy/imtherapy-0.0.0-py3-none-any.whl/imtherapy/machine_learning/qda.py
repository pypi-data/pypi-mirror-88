"""Provide Quantitative Descriptive Analysis machine learning modules
See
https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.qda.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule


class MLQda(MLProcess):
    """Quantitative Descriptive Analysis model"""
    name = 'MLQda'
    args = MLProcess.args.copy()

class MachineLearningQda(MachineLearningModule):
    """Machine Learning module using Quantitative Descriptive Analysis"""
    name = 'qda'
    long = 'Quantitative Descriptive Analysis model'
    model = 'classif.qda'
    process = MLQda

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        self.process.args['factorize_chars'] = True

ml_modules.register(MachineLearningQda())
