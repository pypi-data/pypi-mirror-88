from abc import ABC, abstractproperty
from simplug import Simplug
from .defaults import (
    FEATURE_SELECTION_MODULE_GROUP,
    FEATURE_TRANSFORM_MODULE_GROUP,
    MACHINE_LEARNING_MODULE_GROUP
)

class Module(ABC):

    @abstractproperty
    def start_process(self):
        """"""

    @abstractproperty
    def end_process(self):
        """"""

    def on_args_init(self, params):
        """"""

    def on_args_parsed(self, args):
        """"""

class FTModule(Module):
    ...

class FSModule(Module):
    ...

class MLModule(Module):
    ...

fs_modules = Simplug(FEATURE_SELECTION_MODULE_GROUP)
ft_modules = Simplug(FEATURE_TRANSFORM_MODULE_GROUP)
ml_modules = Simplug(MACHINE_LEARNING_MODULE_GROUP)

for module in (fs_modules, ft_modules, ml_modules):
    module.spec(Module.on_args_init)
    module.spec(Module.on_args_parsed)
    module.load_entrypoints()

def load_builtin_modules():
    """Load the built-in modules"""
    from . import feature_selection, feature_transform, machine_learning
