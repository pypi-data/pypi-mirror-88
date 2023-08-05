"""Provide generic classes for builtin machine learning modules"""
from pipen import Proc
from pyparam.exceptions import PyParamNameError
from ..modules import MLModule
from ..envs import envs
from ..defaults import SCRIPT_DIR


class MLProcess(Proc):
    singleton = True
    input_keys = 'selected_features:file'
    output = 'outdir:file:results'
    script = f'file://{SCRIPT_DIR}/MachineLearning.R'
    envs = envs
    args = {
        'ncores': 1,
        'survs': [],
        'outcome': [],
        'outcome_positive': [],
        # Whether the model requires numeric features
        'factorize_chars': False,
        'model': None,
        'model_name': None,
    }

class MachineLearningModule(MLModule):
    name = None
    long = None
    model = None
    process = None

    @property
    def start_process(self):
        return self.process

    @property
    def end_process(self):
        return self.process

    def _add_param(self, params, *args, **kwargs):
        try:
            params.add_param(*args, **kwargs)
        except PyParamNameError:
            pass

    def on_args_init(self, params):
        self._add_param(
            params,
            'ml',
            type='ns',
            desc=(f'Options for builtin machine learning models. '
                  'Only available when they are selected.')
        )
        self._add_param(
            params,
            'ml.resample',
            default='cv:10',
            argname_shorten=False,
            desc=(
                'Resampling strategy for all builtin machine learning modules.',
                '* `holdout`/`holdout:<ratio>`: '
                'Splits data into a training set and a test set. '
                'Ratio determines the ratio of observation going into '
                'the training set (default: 2/3).',
                '* `cv`/`cv:<fold>`: '
                'Splits data using a folds-folds (default: 10 folds) '
                'cross-validation.',
                '* `loo`: Splits data using leave-one-observation-out.',
                '* `repeated_cv`/`repeated_cv:<repeats>:<fold>`: '
                'Splits data repeats (default: 10) times using '
                'a folds-fold (default: 10) cross-validation.'
            ),
            callback=lambda val: (
                ['holdout', 2./3.]
                if val == 'holdout'
                else ['holdout', float(val.split(':', 1)[1])]
                if val.startswith('holdout:')
                else ['cv', 10]
                if val == 'cv'
                else ['cv', int(val.split(':', 1)[1])]
                if val.startswith('cv:')
                else ['loo']
                if val == 'loo'
                else ['repeated_cv', 10, 10]
                if val == 'repeated_cv'
                else ['repeated_cv',
                      int(val.split(':', 2)[1]),
                      int(val.split(':', 2)[2])]
                if val.startswith('repeated_cv:')
                else ValueError('Unsupported resampleing method.')
            )
        )

    def on_args_parsed(self, args):
        self.process.args['ncores'] = args.ncores
        self.process.args['survs'] = sum([list(survs) for survs in args.survs],
                                         [])
        self.process.args['outcome'] = args.outcome
        self.process.args['outcome_positive'] = args['outcome-positive']
        self.process.args['resample'] = args.ml.resample
        self.process.args['model'] = self.model
        self.process.args['model_name'] = getattr(self, 'long') or self.name
