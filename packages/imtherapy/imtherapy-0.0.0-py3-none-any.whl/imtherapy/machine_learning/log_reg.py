"""Provide Logistic Regression machine learning modules
See https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.log_reg.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule


class MLLogReg(MLProcess):
    """Logistic Regression model"""
    name = 'MLLogReg'
    args = MLProcess.args.copy()

class MachineLearningLogReg(MachineLearningModule):
    """Machine Learning module using Logistic Regression"""
    name = 'log_reg'
    long = 'Logistic Regression'
    model = 'classif.log_reg'
    process = MLLogReg

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        # self.process.args['factorize_chars'] = True

ml_modules.register(MachineLearningLogReg())
