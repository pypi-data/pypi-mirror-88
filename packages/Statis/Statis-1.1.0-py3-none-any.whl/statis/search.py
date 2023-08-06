"""
Functions for searching and listing notifiers in available modules.

A notifier module encapsulates related notifiers of a certain category,
such as 'cpu'. It may be composed of either a package containing actual
Python modules, each providing one :class:`Notifier` class, or a single
module at the root of any search path possibly providing multiple ones.

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import collections
import logging
import pathlib
import re
from itertools import chain
from typing import Dict, Iterator, List, Optional

from statis import module
from statis.notifier import Notifier

SEARCH_PATHS: List[pathlib.Path] = [
    pathlib.Path.home() / '.config/statis/modules',
    pathlib.Path(__file__).parent / 'modules',
]


def find_notifier(module_name: str, notifier_name: str) -> Notifier:
    """
    Search for a notifier and return the first one found.

    In each search path, the following paths are inspected in order:
      1. `<module_name>.py` (may contain multiple `Notifier` classes)
      2. `<module_name>/<notifier_name>.py` (should contain only one
         `Notifier` class whose name matches the file in PascalCase)

    :param module_name: A module containing the notifier to find
    :param notifier_name: The notifier (same as module if empty)
    :return: An instance of the first found notifier

    :raises FileNotFoundError: if the given notifier does not exist
    """
    module_name = _to_module_filename(module_name)
    usage_cmd_name: str = module_name

    if notifier_name:
        notifier_name = _to_module_filename(notifier_name)
        usage_cmd_name += f' {notifier_name}'
    else:
        notifier_name = module_name

    logging.info('Searching potential paths of notifier "%s" in '
                 'module "%s"...', notifier_name, module_name)

    paths_to_inspect: Iterator[pathlib.Path] = chain.from_iterable(
        ((p / module_name), (p / module_name / notifier_name))
        for p in SEARCH_PATHS)

    class_name: str = _snake_to_pascal_case(notifier_name)

    for path in paths_to_inspect:
        path = path.with_suffix('.py')
        if not path.exists():
            logging.debug('Path does not exist: %s', path)
            continue

        logging.info('Found path: %s', path)

        notifier_class = module.get_notifier(class_name, path)
        if notifier_class is not None:
            notifier: Notifier = notifier_class()
            notifier.set_command_name(usage_cmd_name)
            return notifier

        logging.info('Continuing search...')

    raise FileNotFoundError(f'Notifier "{notifier_name}" in module '
                            f'"{module_name}" could not be found.')


def list_all() -> Dict[str, List[str]]:
    """
    Return a dict of modules mapped to their contained notifiers.

    Example:
      {'battery': ['charge', 'capacity'], 'cpu': ['temp', 'usage']}

    :return: A dict mapping modules to their contained notifiers
    """
    notifiers_by_module: Dict[str, List[str]] = collections.defaultdict(list)

    for package, module_paths in _find_modules_per_package().items():
        for path in sorted(module_paths, key=lambda p: p.name):
            module_name: str = path.stem.replace('_', '-')

            if package is not None:
                class_name: str = _snake_to_pascal_case(path.stem)
                if module.get_notifier(class_name, path) is not None:
                    notifiers_by_module[package].append(module_name)
            else:
                notifier_names: List[str] = module.list_notifiers(path)
                if notifier_names:
                    notifiers_by_module[module_name].extend(notifier_names)

    return notifiers_by_module


def _find_modules_per_package() -> Dict[Optional[str], List[pathlib.Path]]:
    """
    Return a dict of packages mapped to their contained Python modules.

    Modules are collected across all search paths. Files located at the
    root of a search path are stored under a `None` key.

    :return: A dict mapping packages to their contained Python modules
    """
    modules_by_package: Dict[
        Optional[str], List[pathlib.Path]] = collections.defaultdict(list)

    for search_path in SEARCH_PATHS:
        for module_file in search_path.glob('**/*.py'):
            parent_package: Optional[str] = None
            if module_file.parent.resolve() != search_path.resolve():
                parent_package = module_file.parent.name.replace('_', '-')

            modules_by_package[parent_package].append(module_file)

    return modules_by_package


def _to_module_filename(string: str) -> str:
    """
    Normalize the given string to a valid module/package name.

    Examples:
      >>> _to_module_filename('cpu-usage')
      'cpu_usage'
      >>> _to_module_filename('Cpu_Usage')
      'cpu_usage'
      >>> _to_module_filename('cpu&?usage')
      'cpu_usage'

    :param string: A string to derive a module name from
    :return: The given string as a valid module name
    """
    return re.sub(r'\W+', '_', string).lower()


def _snake_to_pascal_case(string: str) -> str:
    """
    Convert the given string from snake_case to PascalCase.

    Examples:
      >>> _snake_to_pascal_case('cpu_usage')
      'CpuUsage'
      >>> _snake_to_pascal_case('volume')
      'Volume'

    :param string: A snake_case string to convert
    :return: The given string in PascalCase
    """
    return string.replace('_', ' ').title().replace(' ', '')
