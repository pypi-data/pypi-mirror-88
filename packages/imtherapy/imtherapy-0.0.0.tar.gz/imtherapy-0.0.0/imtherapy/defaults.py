from pathlib import Path
from pyparam import defaults as pyparam_defaults

# adjust cli help page
pyparam_defaults.CONSOLE_WIDTH = 100
pyparam_defaults.HELP_OPTION_WIDTH = 36

PIPELINE_OPTION_TITLE = 'PIPELINE_OPTIONS'
FEATURE_TRANSFORM_MODULE_GROUP = 'imtherapy-feature-transform'
FEATURE_SELECTION_MODULE_GROUP = 'imtherapy-feature-selection'
MACHINE_LEARNING_MODULE_GROUP = 'imtherapy-machine-learning'

PIPELINE_DESCRIPTION = (
    'A framework to explore, select and discover predictive markers '
    'for cancer immunotherapy'
)

# other constants
SCRIPT_DIR = Path(__file__).parent.joinpath('scripts').resolve()
REPORT_DIR = Path(__file__).parent.joinpath('reports').resolve()
