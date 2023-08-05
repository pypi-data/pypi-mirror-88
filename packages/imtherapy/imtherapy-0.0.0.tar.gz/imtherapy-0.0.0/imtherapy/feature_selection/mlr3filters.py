"""Provide filter for feature selection"""
from pipen import Proc
from ..modules import FSModule, fs_modules
from ..envs import envs
from ..defaults import SCRIPT_DIR

class FSMlr3Filters(Proc):
    """Use mlr3filters for feature selection"""
    name = 'FeatureSelectMlr3Filters'
    singleton = True
    input_keys = 'infile:file'
    output = 'outfile:file:selected-{{in.infile | bn}}'
    script = f'file://{SCRIPT_DIR}/FSMlr3Filters.R'
    envs = envs
    args = {}

class FeatureSelectionMlr3FiltersModule(FSModule):
    """Feature selection module using mlr3filters package"""
    name = 'mlr3filters'
    process = FSMlr3Filters
    start_process = end_process = FSMlr3Filters

    @fs_modules.impl
    def on_args_init(self, params):
        params.add_param(
            'mlr3filters',
            type='ns',
            desc=('Options for mlr3filters feature selection module. '
                  'Only available when it is selected.')
        )
        params.add_param(
            'mlr3filters.filter',
            argname_shorten=False,
            type=str,
            show=False,
            default='auc',
            desc=('The filter method. '
                  'See https://mlr3filters.mlr-org.com/ '
                  'for available filters.')
        )
        params.add_param(
            'mlr3filters.cutoff',
            argname_shorten=False,
            type=float,
            show=False,
            default=0.05,
            desc=('The cutoff to select the features. '
                  'Scores are min-max scaled in 0~1.')
        )
        params.add_param(
            'mlr3filters.learner',
            argname_shorten=False,
            type=str,
            show=False,
            default='classif.ranger',
            desc=('The learner for importance filter, used only when '
                  '--mlr3filters.filter is `importance`.')
        )
        params.add_param(
            'mlr3filters.params',
            argname_shorten=False,
            type='json',
            show=False,
            desc=('Paramters for the filter. '
                  'You would usually see them by `filter_cor$param_set$values`.'
                  ' For available learners with variable '
                  'importance enabled, ',
                  'See: https://mlr3book.mlr-org.com/list-filters.html')
        )

    @fs_modules.impl
    def on_args_parsed(self, args):
        self.process.lang = args.rscript
        self.process.args['filter'] = args.mlr3filters.filter
        self.process.args['cutoff'] = args.mlr3filters.cutoff
        self.process.args['params'] = args.mlr3filters.params
        self.process.args['learner'] = args.mlr3filters.learner
        self.process.args['ncores'] = args.ncores
        self.process.args['outcome'] = args.outcome
        self.process.args['survs'] = args.survs
        self.process.args['outcome_positive'] = args['outcome-positive']

fs_modules.register(FeatureSelectionMlr3FiltersModule())
