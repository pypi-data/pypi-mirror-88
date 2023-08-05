"""A framework to explore, select and discover predictive markers for
cancer immunotherapy"""
import sys

from pyparam import params
from pyparam.exceptions import PyParamValueError
from pipen_args import Args

from .defaults import PIPELINE_OPTION_TITLE, PIPELINE_DESCRIPTION
from .modules import (
    ft_modules,
    fs_modules,
    ml_modules,
    load_builtin_modules
)
from .commands import full_opts, list_modules

# Load all built-in modules
load_builtin_modules()

params = Args(pipen_opt_group=PIPELINE_OPTION_TITLE,
              desc=[PIPELINE_DESCRIPTION,
                    'See full options by `{prog} full-opts`'])
opts_to_hide = (
    'profile',
    'loglevel',
    'dirsig',
    'cache',
    'forks',
    'workdir',
    'error_strategy',
    'num_retries',
    'submission_batch',
    'envs',
    'scheduler',
    'scheduler_opts',
    'plugins',
    'plugin_opts'
)
for opt in opts_to_hide:
    params.get_param(opt).show = False

params.add_command(
    'full-opts',
    'Show full options',
    help_on_void=False
)
params.add_command(
    'list-fs-modules',
    'List all feature selection modules.',
    help_on_void=False
)
params.add_command(
    'list-ft-modules',
    'List all feature tranformation modules.',
    help_on_void=False
)
params.add_command(
    'list-ml-modules',
    'List all machine learning modules.',
    help_on_void=False
)
params.add_param(
    'i,infile',
    type='path',
    desc='Input file with direct features and outcomes',
    required=True
)
params.add_param(
    's,feat-select',
    type='choice',
    desc='Feature selection module to use. One of {choices}',
    default='use-all',
    choices=fs_modules.get_enabled_plugin_names(),
    callback=lambda val, all_vals: (
        ValueError('Feature selection module other than use-all only works '
                   'with single outcome.')
        if val != 'use-all' and len(all_vals.outcome) > 1
        else val
    )
)
params.add_param(
    't,feat-transforms',
    type='list',
    desc='Feature transformation modules to use. Avaiable: {}.'.format(
        ', '.join(module for module in ft_modules.get_all_plugin_names()
                  if module != 'direct')
    ),
)
params.add_param(
    'm,machine-learning',
    type='list',
    desc='Machine learning modules to use. Avaiable: {}'.format(
        ', '.join(module for module in ml_modules.get_all_plugin_names())
    ),
    required=True
)
params.add_param(
    'survs',
    type='list',
    desc=('The time and event columns for survival '
          'analysis. Multiple time-event column pairs are supported.'
          'For example, --survs OFS_time OFS_event --survs PFS_time PFS_event'),
    callback=lambda val: (
        ValueError('Expect pairs of time-event columns')
        if len(val) % 2 != 0
        else [(val[i], val[i+1]) for i in range(0, len(val), 2)]
    )
)
params.add_param(
    'outcome',
    type='list',
    required=True,
    desc=('The column name of the outcome. '
          'You can have multiple outcome columns. For example, '
          '--outcome "Clinic Benefits" --outcome Response')
)
params.add_param(
    'ncores',
    type=int,
    default=1,
    desc=('Number of cores to use for wherever parallelization applies.')
)
params.add_param(
    'outcome-positive',
    type='list',
    desc=('Which level of outcome we are predicting.'
          'When specified, it should match '
          'the number of elements in --outcome.'),
    callback=lambda val, all_vals: (
        ValueError(f'Unmatched number of elements ({len(val)}) '
                   f'with that of --outcome ({len(all_vals.outcome)})')
        if val and len(val) != len(all_vals.outcome)
        else val
    )
)
params.add_param(
    'rscript',
    show=False,
    default='Rscript',
    desc='The path to Rscript to run processes with scripts in R.'
)
params.add_param(
    'ffr-feats',
    show=False,
    type='list',
    desc=('Features for feature-feature relationship investigation. '
          'Default will only investigate the selected features. '
          'You can also add direct transformed features.')
)
params.add_param(
    'uni-feats',
    show=False,
    type='list',
    desc=('Features for univariate statistical analysis. '
          'Default will only explore the selected features. '
          'You can also add direct transformed features.')
)
params.add_param(
    'surv-feats',
    show=False,
    type='list',
    desc=('Features for survival analysis. '
          'Default will only explore the selected features. '
          'You can also add direct transformed features.')
)
params.add_param(
    'surv-unit',
    show=False,
    type='str',
    default='Days',
    desc=('The unit for the survival time, used to show on the plots.')
)
params.add_param(
    'metric-avg',
    show=False,
    type='choice',
    default='macro',
    choices=['micro', 'macro'],
    desc=('Method for aggregation:',
          '* `micro`: All predictions from multiple resampling iterations '
          'are first combined into a single Prediction object. Next, the '
          'scoring function of the measure is applied on this combined object, '
          'yielding a single numeric score.',
          '* `macro`: The scoring function is applied on the Prediction object '
          'of each resampling iterations, each yielding a single numeric '
          'score. Next, the scores are combined with the aggregator function '
          'to a single numerical score.',
          'See more details here: ',
          'https://mlr3.mlr-org.com/reference/Measure.html?q=average')
)
params.add_param(
    'missing',
    type='choice',
    default='impute',
    choices=['impute', 'discard', 'drop'],
    desc=(
        'How to deal with the missing data. This applies before features '
        'are selected. ',
        '* `impute`: Use the R package to do the imputation. See: '
        'https://github.com/ModelOriented/EMMA/tree/master/NADIA_package/NADIA',
        'This is only applicable when you have only one outcome in the input '
        'dataset.',
        '* `discard`/`drop`: Discard the records for downstream analysis. '
        'For single variate analysis, only discard the record with the value '
        'of that variate missing.'
    ),
    callback=lambda val, all_vals: (
        ValueError('Impute missing data can only work with single outcome.')
        if val == 'impute' and len(all_vals.outcome) > 1
        else val
    )
)


params.param_groups[PIPELINE_OPTION_TITLE] = params.param_groups.pop(
    PIPELINE_OPTION_TITLE
)

ft_modules.hooks.on_args_init(params)
fs_modules.hooks.on_args_init(params)
ml_modules.hooks.on_args_init(params)

args = params.parse(ignore_errors=True)

if args.__command__ == 'full-opts':
    full_opts(params)
    sys.exit(0)
elif args.__command__ == 'list-fs-modules':
    list_modules(fs_modules, 'Feature selection modules')
    sys.exit(0)
elif args.__command__ == 'list-ft-modules':
    list_modules(ft_modules, 'Feature transformation modules')
    sys.exit(0)
elif args.__command__ == 'list-ml-modules':
    list_modules(ml_modules, 'Machine learning modules')
    sys.exit(0)

else:
    args = params.parse()
    ft_modules.hooks.on_args_parsed(args)
    fs_modules.hooks.on_args_parsed(args)
    ml_modules.hooks.on_args_parsed(args)
