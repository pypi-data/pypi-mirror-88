"""SVM machine learning modules
See
https://mlr3learners.mlr-org.com/reference/mlr_learners_classif.svm.html
"""
from ..modules import ml_modules
from ._generic import MLProcess, MachineLearningModule

class MLSvm(MLProcess):
    """SVM"""
    name = 'MLSvm'
    args = MLProcess.args.copy()

class MachineLearningSvm(MachineLearningModule):
    """Machine Learning module using SVM"""
    name = 'svm'
    long = 'SVM'
    model = 'classif.svm'
    process = MLSvm

    @ml_modules.impl
    def on_args_init(self, params):
        super().on_args_init(params)

    @ml_modules.impl
    def on_args_parsed(self, args):
        super().on_args_parsed(args)
        self.process.args['factorize_chars'] = True

ml_modules.register(MachineLearningSvm())
