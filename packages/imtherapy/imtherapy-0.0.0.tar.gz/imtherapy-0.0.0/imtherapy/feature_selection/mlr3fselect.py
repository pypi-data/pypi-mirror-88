"""Provide module using mlr3fselect for feature selection"""
from pipen import Proc
from ..modules import FSModule, fs_modules
from ..envs import envs
from ..defaults import SCRIPT_DIR

class FSMlr3FSelect(Proc):
    """Use mlr3fselect for feature selection"""
    name = 'FeatureSelectMlr3FSelect'
    singleton = True
    input_keys = 'infile:file'
    output = 'outfile:file:selected-{{in.infile | bn}}'
    script = f'file://{SCRIPT_DIR}/FSMlr3FSelect.R'
    envs = envs
    args = {}

class FeatureSelectionMlr3FSelectModule(FSModule):
    """Feature selection module using mlr3fselect package"""
    name = 'mlr3fselect'
    process = FSMlr3FSelect
    start_process = end_process = FSMlr3FSelect

    @fs_modules.impl
    def on_args_init(self, params):
        params.add_param(
            'mlr3fselect',
            type='ns',
            desc=('Options for mlr3fselect feature selection module. '
                  'Only available when it is selected.',
                  'See https://mlr3fselect.mlr-org.com/')
        )
        params.add_param(
            'mlr3fselect.resample',
            default='cv:10',
            show=False,
            argname_shorten=False,
            desc=(
                'Resampling strategy.',
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
        params.add_param(
            'mlr3fselect.learner',
            type=str,
            show=False,
            default='classif.rpart',
            argname_shorten=False,
            desc=('The learner for mlr3fselect')
        )
        params.add_param(
            'mlr3fselect.measure',
            type=str,
            show=False,
            default='classif.ce',
            argname_shorten=False,
            desc=('The measurement for mlr3fselect.')
        )
        params.add_param(
            'mlr3fselect.terminator',
            type=str,
            show=False,
            default='evals:20',
            argname_shorten=False,
            desc=('The terminator for mlr3fselect.')
        )
        params.add_param(
            'mlr3fselect.selector',
            type=str,
            show=False,
            default='random_search',
            argname_shorten=False,
            desc=('The selector for mlr3fselect.')
        )

    @fs_modules.impl
    def on_args_parsed(self, args):
        self.process.lang = args.rscript
        self.process.args['resample'] = args.mlr3fselect.resample
        self.process.args['learner'] = args.mlr3fselect.learner
        self.process.args['measure'] = args.mlr3fselect.measure
        self.process.args['terminator'] = args.mlr3fselect.terminator
        self.process.args['selector'] = args.mlr3fselect.selector
        self.process.args['ncores'] = args.ncores
        self.process.args['outcome'] = args.outcome
        self.process.args['survs'] = args.survs
        self.process.args['outcome_positive'] = args['outcome-positive']

fs_modules.register(FeatureSelectionMlr3FSelectModule())
