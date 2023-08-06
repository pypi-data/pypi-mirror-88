"""
Command line argument parsing and logging configuration.

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
import logging
import re
import sys
from typing import List, Match, Optional, Union

from statis import notification
from statis._version import __version__
from statis.monitor import Threshold

THRESHOLD_PATTERN = re.compile(r'([<>]?=?)(\d+(?:\.\d+)?)([^.\s\d]+)')


def _get_threshold(string: str) -> Union[Threshold, bool]:
    """
    Parse the given threshold argument to a :class:`Threshold`.

    The string (ignoring whitespace) may be
      a) in the format "[<|>][=] <value> <unit>" or
      b) empty, in which case `False` is returned.

    :param string: The argument string to return a threshold for
    :return: A threshold or `False` if the given string is empty
    :raises ArgumentTypeError: if the given string is invalid
    """
    string = ''.join(string.split())

    if not string:
        return False

    match: Optional[Match] = THRESHOLD_PATTERN.match(string)
    if match is not None:
        type_symbol = match.group(1)
        if type_symbol:
            threshold_type = Threshold.Type(type_symbol)
        else:
            threshold_type = Threshold.Type.ABOVE

        value: float = float(match.group(2))
        unit: str = match.group(3)
        return Threshold(value, unit, threshold_type)

    raise argparse.ArgumentTypeError('Threshold must be given as: '
                                     '"[<|>][=] <value> <unit>"')


def parse_args(arg_list: List[str]) -> argparse.Namespace:
    """
    Parse and return any provided command line arguments.

    :return: A namespace holding all parsed arguments
    """
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] [module [notifier] [notifier_args...]]',
        description='Modular system monitoring and status display via '
                    'desktop notifications.',
        epilog='examples:\n'
               '  %(prog)s cpu usage --core 2\n'
               '  %(prog)s memory free\n'
               '  %(prog)s time',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('module', nargs='?',
                        help='the module of which to run a notifier (e.g. '
                             '\033[3mcpu\033[0m)')
    parser.add_argument('notifier', nargs='?', default='',
                        help='the notifier to run (equal to <\033[1mmodule'
                             '\033[0m> if empty)')
    parser.add_argument('notifier_args', nargs=argparse.REMAINDER,
                        help='any arguments specific to the given notifier')

    parser.add_argument('-l', '--list', action='store_true',
                        help='list all available notifiers grouped by module')
    parser.add_argument('-t', '--timeout', type=float, metavar='N', default=3,
                        help='time in seconds until the notification expires\n'
                             '(default: %(default).1f)')
    parser.add_argument('-u', '--urgency', type=str.lower, metavar='str',
                        default=notification.Urgency.LOW.value,
                        choices=[u.value for u in notification.Urgency],
                        help='an urgency level to send the notification with\n'
                             'one of: {%(choices)s} (default: %(default)s)')

    m_group = parser.add_argument_group(title='monitoring options')
    m_group.add_argument('-m', '--monitor', type=_get_threshold, metavar='str',
                         help='begin monitoring and notify at the given '
                              'threshold\nformat: "[<|>][=] <value> <unit>"; '
                              'e.g. ">= 8 GB"\nmay be an empty string \033[3m'
                              '""\033[0m to notify on all changes')
    m_group.add_argument('-p', '--polling-rate', type=float, metavar='N',
                         help='polling rate in seconds to use for monitoring\n'
                              '(applies only to polling-based monitors)')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help="print additional messages on what's being done")
    parser.add_argument('-d', '--debug', action='store_true',
                        help='print detailed logs to aid in debugging')
    parser.add_argument('-V', '--version', action='version',
                        version=f'%(prog)s {__version__}')

    args: argparse.Namespace = parser.parse_args(arg_list)

    if not args.list and args.module is None:
        parser.print_help()
        sys.exit(2)

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    return args


def setup_logging() -> None:
    """
    Configure the logging format to include colored [level] prefixes.
    """
    logging.basicConfig(format='[%(levelname)s\033[0m] %(message)s')

    logging.addLevelName(logging.DEBUG, '\033[1;35mD')
    logging.addLevelName(logging.INFO, '\033[1;34mI')
    logging.addLevelName(logging.WARNING, '\033[1;33mW')
    logging.addLevelName(logging.ERROR, '\033[1;31mE')
    logging.addLevelName(logging.CRITICAL, '\033[1;31mC')
