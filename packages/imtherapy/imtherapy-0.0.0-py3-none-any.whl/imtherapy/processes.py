"""Common processes"""
from os import path
from pipen import Proc
from pipen.channel import flatten

from .envs import envs
from .defaults import SCRIPT_DIR, REPORT_DIR

class UnivariateStatisticAnalysis(Proc):
    """Investigating the features against the outcome individually.

    Requires ggplot2, GGally and tidystats in R
    """
    name = 'UnivariateStatisticAnalysis'
    input_keys = 'selected_features:file, merged_features:file'
    output = 'outdir:file:univariate'
    script = f'file://{SCRIPT_DIR}/UnivariateStatisticAnalysis.R'
    envs = envs
    plugin_opts = {
        'report': f'file://{REPORT_DIR}/UnivariateStatisticAnalysis.svx'
    }

class SurvivalAnalysis(Proc):
    """Survival analysis for the features.

    Requires survival, survminer and tidystats packages in R."""
    name = 'SurvivalAnalysis'
    input_keys = 'selected_features:file, merged_features:file'
    output = 'unidir:file:univariate, multidir:file:multivariate'
    script = f'file://{SCRIPT_DIR}/SurvivalAnalysis.R'
    envs = envs
    plugin_opts = {
        'report': f'file://{REPORT_DIR}/SurvivalAnalysis.svx'
    }

class FeatureFeatureRelationship(Proc):
    """Exploring relationships between features.

    Requires ggplot2, GGally and tidystats in R
    """
    name = 'FeatureFeatureRelationship'
    input_keys = 'selected_features:file, merged_features:file'
    output = 'outdir:file:relationships'
    script = f'file://{SCRIPT_DIR}/FeatureFeatureRelationship.R'
    envs = envs
    plugin_opts = {
        'report': f'file://{REPORT_DIR}/FeatureFeatureRelationship.svx'
    }

class PredictionMetrics(Proc):
    """Metrics and plots for prediction results"""
    name = 'PredictionMetrics'
    input_keys = 'predirs:files'
    input = lambda ch: ch >> flatten()
    output = 'outdir:file:metrics'
    script = f'file://{SCRIPT_DIR}/PredictionMetrics.R'
    envs = envs
    plugin_opts = {
        'report': f'file://{REPORT_DIR}/PredictionMetrics.svx'
    }

class MergeTransformedFeatures(Proc):
    """Merge all transformed features"""
    name = 'MergeTransformedFeatures'
    singleton = True
    input_keys = 'transformed_features:files'
    input = lambda ch: ch >> flatten()
    output = 'outfile:file:merged-features.txt'
    script = f'file://{SCRIPT_DIR}/MergeTransformedFeatures.R'
    envs = envs

class ImputeMissingData(Proc):
    """Impute missing data using mice package"""
    name = "ImputeMissingData"
    singleton = True
    input_keys = 'merged_features:file'
    output = 'outfile:file:imputed-data.txt'
    script = f'file://{SCRIPT_DIR}/ImputeMissingData.R'
    envs = envs
    plugin_opts = {
        'report': f'file://{REPORT_DIR}/ImputeMissingData.svx'
    }


class FileToProcess(Proc):
    input_keys = 'infile:file'
    output = 'outfile:file:{{in.infile | bn}}'
    script = 'ln -fs {{in.infile | abspath}} {{out.outfile}}'
    envs = envs
