"""Provide use-all feature selection module"""
from ..modules import FSModule, fs_modules
from ..processes import FileToProcess

class FSUseAll(FileToProcess):
    """Use all the features for ML"""
    name = 'FeatureSelectUseAll'
    singleton = True

class FeatureSelectionUseAll(FSModule):
    """A proxy module for feature selection that actually uses all the features.
    """
    name = 'use-all'
    start_process = end_process = FSUseAll

fs_modules.register(FeatureSelectionUseAll())
