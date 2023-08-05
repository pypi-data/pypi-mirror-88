import pkgutil
from textwrap import dedent

def load_submodules(name, path, excludes=None):
    excludes = excludes or []
    for _, modname, _ in pkgutil.walk_packages(path):
        if modname in excludes:
            continue
        __import__(f'{name}.{modname}')

def text_dedent(text):
    splits = text.split('\n', 1)
    if len(splits) > 1:
        first_line, rest = splits
        return f"{first_line}\n{dedent(rest)}"
    return splits[0]
