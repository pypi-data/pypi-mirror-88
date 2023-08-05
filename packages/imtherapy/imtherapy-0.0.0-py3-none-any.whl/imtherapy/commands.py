from rich.console import Console
from rich.table import Table

from .utils import text_dedent

def full_opts(params):
    for key, val in params.params.items():
        val.show = True

    params.print_help()

def list_modules(modules, module_type):
    console = Console()
    modules = modules.get_all_plugins(raw=True)
    table = Table(title=module_type)
    table.add_column('Name')
    table.add_column('Description')

    for name, module in modules.items():
        table.add_row(
            name,
            text_dedent(module.__doc__).rstrip()
            if getattr(module, '__doc__', None)
            else '-'
        )

    console.print(table)

