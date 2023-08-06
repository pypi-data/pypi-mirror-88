"""
Functions for module import and retrieval of contained notifiers.

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import importlib.util
import inspect
import logging
import pathlib
import re
from types import ModuleType
from typing import Any, List, Optional, Tuple, Type

from statis.notifier import Notifier


def get_notifier(class_name: str,
                 module_path: pathlib.Path) -> Optional[Type[Notifier]]:
    """
    Retrieve a :class:`Notifier` in the given Python module.

    :param class_name: The name of the notifier subclass to retrieve
    :param module_path: The file path of the module containing it
    :return: A notifier subclass or None if it does not exist

    :raises FileNotFoundError: if the module path does not exist
    """
    module: ModuleType = _import_module(module_path)
    attr: Optional[Any] = getattr(module, class_name, None)

    if attr is None or not inspect.isclass(attr):
        logging.info('Module "%s" does not contain a "%s" class.',
                     module_path.name, class_name)
        return None

    if not issubclass(attr, Notifier):
        logging.warning('Class "%s" in "%s" does not extend Notifier.',
                        class_name, module_path.name)
        return None

    return attr


def list_notifiers(module_path: pathlib.Path) -> List[str]:
    """
    Return the CLI names for all notifiers in the given Python module.

    These are the notifiers' class names in kebab-case, which are used
    on the CLI to specify the one to run. For example, a notifier class
    `AvgUsage` in the module `cpu` would be invoked via `cpu avg-usage`.

    :param module_path: The file path of the module to list notifiers in
    :return: A list of CLI names for all notifiers in the given module
    :raises FileNotFoundError: if the module path does not exist
    """
    module: ModuleType = _import_module(module_path)
    classes: List[Tuple[str, Type]] = inspect.getmembers(module,
                                                         inspect.isclass)
    return [_cli_name_for_class(class_name) for (class_name, c) in classes
            if issubclass(c, Notifier) and c.__module__ == module.__name__]


def _import_module(module_path: pathlib.Path) -> ModuleType:
    """
    Import a Python module from the given path.

    :param module_path: The file path of the module to import
    :return: The imported module
    :raises FileNotFoundError: if the module path does not exist
    """
    if not module_path.exists():
        raise FileNotFoundError(f'Failed to import module from '
                                f'non-existent path: {module_path}')

    module_name: str = re.sub(r'\W+', '_', module_path.with_suffix('').name)

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def _cli_name_for_class(class_name: str) -> str:
    """
    Return the given class's hyphenated name for CLI usage.

    Examples:
      >>> _cli_name_for_class('AvgUsage')
      'avg-usage'
      >>> _cli_name_for_class('Volume')
      'volume'

    :param class_name: A notifier class's name in PascalCase
    :return: The CLI name to use for invoking the notifier
    """
    return re.sub('(?!^)([A-Z]+)', r'-\1', class_name).lower()
