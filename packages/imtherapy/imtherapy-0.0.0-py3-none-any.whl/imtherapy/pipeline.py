"""A framework to explore, select and discover predictive markers for
cancer immunotherapy"""
from pipen import Pipen

from .defaults import PIPELINE_DESCRIPTION
from .args import args
from .modules import (
    ft_modules,
    fs_modules,
    ml_modules
)
from .processes import (
    UnivariateStatisticAnalysis,
    SurvivalAnalysis,
    FeatureFeatureRelationship,
    PredictionMetrics,
    MergeTransformedFeatures,
    ImputeMissingData
)

def get_feature_transform_processes():
    feature_transform_modules = ft_modules.get_enabled_plugins(raw=True)
    starts = []
    ends = []
    for name, ft_module in feature_transform_modules.items():
        if name not in args.t and name != 'direct':
            continue
        if isinstance(ft_module.start_process, (tuple, list)):
            starts.extend(ft_module.start_process)
        else:
            starts.append(ft_module.start_process)

        ends.append(ft_module.end_process)
    return starts, ends

def get_feature_merge_process(requires):
    merge_proc = MergeTransformedFeatures(
        lang=args.rscript,
        requires=requires
    )
    if args.missing == 'impute':
        impute_proc = ImputeMissingData(
            lang=args.rscript,
            requires=merge_proc,
            args={'outcome': args.outcome,
                  'survs': args.survs,
                  'outcome_positive': args['outcome-positive']}
        )
        return [impute_proc]
    return [merge_proc]

def get_feature_select_processes(requires):
    feature_selection_module = fs_modules.get_plugin(args.s, raw=True)
    feature_selection_module.start_process(requires=requires)
    end = feature_selection_module.end_process
    return [end]

def get_machine_learning_processes(requires):
    machine_learning_module = ml_modules.get_enabled_plugins(raw=True)
    ends = []
    for name, ml_module in machine_learning_module.items():
        if name not in args.m:
            continue
        if isinstance(ml_module.start_process, (tuple, list)):
            for start_process in ml_module.start_process:
                start_process(lang=args.rscript, requires=requires)
        ml_module.start_process(lang=args.rscript, requires=requires)

        ends.append(ml_module.end_process)

    return ends

def get_univariate_analysis_process(requires):

    proc = UnivariateStatisticAnalysis(
        lang=args.rscript,
        requires=requires,
        args={'features': args['uni-feats'],
              'outcome': args.outcome,
              'survs': args.survs}
    )
    return [proc]

def get_survival_analysis_process(requires):
    if args.survs:
        proc = SurvivalAnalysis(
            lang=args.rscript,
            requires=requires,
            args={'features': args['surv-feats'],
                  'outcome': args.outcome,
                  'surv-unit': args['surv-unit'],
                  'survs': args.survs}
        )
        return [proc]
    return None

def get_feature_feature_process(requires):

    proc = FeatureFeatureRelationship(
        lang=args.rscript,
        requires=requires,
        args={'features': args['ffr-feats'],
              'outcome': args.outcome,
              'survs': args.survs}
    )
    return [proc]

def get_prediction_metrics_process(requires):

    proc = PredictionMetrics(
        requires=requires,
        lang=args.rscript,
        args={'average': args['metric-avg'],
              'outcome': args['outcome'],
              'outcome_positive': args['outcome-positive']}
    )
    return [proc]

def pipeline():
    """Get the pipeline object"""
    ft_starts, ft_ends = get_feature_transform_processes()
    fm_ends = get_feature_merge_process(ft_ends)
    fs_ends = get_feature_select_processes(fm_ends)
    ml_ends = get_machine_learning_processes(fs_ends)
    uv_ends = get_univariate_analysis_process(fs_ends + fm_ends)
    sa_ends = get_survival_analysis_process(fs_ends + fm_ends)
    ff_ends = get_feature_feature_process(fs_ends + fm_ends)
    pm_ends = get_prediction_metrics_process(ml_ends)

    return Pipen(
        'imtherapy',
        desc=PIPELINE_DESCRIPTION,
        plugin_opts={'report': False}
    ).starts(ft_starts)
