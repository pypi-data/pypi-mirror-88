"""Provide merge feature transform module"""
from ..defaults import SCRIPT_DIR
from ..processes import FileToProcess
from ..modules import ft_modules, FTModule
from ..envs import envs

class MergeOtherFeatures(FileToProcess):
    """Merge other direct features"""
    input_keys = 'infiles:files'
    output = 'outfile:file:other-direct-features.txt'
    script = f'file://{SCRIPT_DIR}/MergeOtherFeatures.R'
    envs = envs

class FeatureTransformMergeOtherFeatures(FTModule):
    """A feature transform module that merges other direct features"""
    name = 'merge'
    start_process = end_process = MergeOtherFeatures

    @ft_modules.impl
    def on_args_init(self, params):
        params.add_param(
            'featfiles',
            desc=('Other feature files. Must have the same set '
                  'of row names as --infile do'),
            type=list,
            callback=lambda val, all_vals: (
                ValueError('No feature files specified.')
                if not val and self.name in all_vals.t
                else val
            )
        )

    @ft_modules.impl
    def on_args_parsed(self, args):
        MergeOtherFeatures.lang = args.rscript
        MergeOtherFeatures.input = [args.featfiles]

ft_modules.register(FeatureTransformMergeOtherFeatures())
