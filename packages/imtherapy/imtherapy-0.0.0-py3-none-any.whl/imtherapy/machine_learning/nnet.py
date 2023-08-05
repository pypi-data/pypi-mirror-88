"""Provide Single Layer Neural Network machine learning modules
See
https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.nnet.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule


class MLNnet(MLProcess):
    """Single Layer Neural Network model"""
    name = 'MLNnet'
    args = MLProcess.args.copy()

class MachineLearningNnet(MachineLearningModule):
    """Machine Learning module using Single Layer Neural Network"""
    name = 'nnet'
    long = 'Single Layer Neural Network'
    model = 'classif.nnet'
    process = MLNnet

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        # self.process.args['factorize_chars'] = True

# nnet not implemented in mlr3learners 0.4.2 yet.
# ml_modules.register(MachineLearningNnet())
