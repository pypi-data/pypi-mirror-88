"""Provide module to pass by direct features"""
from ..processes import FileToProcess
from ..modules import ft_modules, FTModule

class DirectFeatures(FileToProcess):
    """Send input file to merge with other transformed features."""

class FeatureTransformDirectFeatures(FTModule):
    """Use all features directly from input file.
    The input file should also include outcomes.
    """
    name = 'direct'
    start_process = end_process = DirectFeatures

    @ft_modules.impl
    def on_args_parsed(self, args):
        DirectFeatures.input = [args.infile]

ft_modules.register(FeatureTransformDirectFeatures())
