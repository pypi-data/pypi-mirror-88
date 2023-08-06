"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
from datetime import date

from statis.notification import Notification
from statis.notifier import Notifier


def _format_today(format_str: str) -> str:
    """
    Return today's date in the given format or as ISO 8601.

    :param format_str: A strftime format (ISO used if empty)
    :return: Today's date in the given format or as ISO 8601
    """
    if not format_str:
        return date.today().isoformat()

    return date.today().strftime(format_str)


class Date(Notifier):
    """A notifier for today's date with customizable formatting."""

    def __init__(self) -> None:
        super().__init__()

        self._format: str = ''
        self._title: str = ''

    def description(self) -> str:
        return 'Display the current date.'

    def add_args(self) -> None:
        self.parser.add_argument('-f', '--format',
                                 metavar='str', default='',
                                 help='a \033[3mstrftime\033[0m-compatible '
                                      'date format\n(default: ISO 8601)')
        self.parser.add_argument('-t', '--title',
                                 metavar='str', default='Date',
                                 help='a title to use for the notification\n'
                                      '(default: "%(default)s")')

        self.parser.epilog = ('example formats:\n'
                              '  %(prog)s -f "%%B %%d"   -> "March 20"\n'
                              '  %(prog)s -f "Week %%W" -> "Week 12"\n\n'
                              'common format codes:\n'
                              '  %%d - Day of the month\n'
                              '  %%m - Month as zero-padded number\n'
                              '  %%b - Month as abbreviated name\n'
                              '  %%B - Month as full name\n'
                              '  %%Y - Year with century (4 digits)\n'
                              '  %%W - Week number starting Monday\n'
                              '  %%x - Date format based on locale\n\n'
                              'See https://strftime.org/ for a complete list '
                              'of format codes.')

    def handle_args(self, args: argparse.Namespace) -> None:
        self._format = args.format
        self._title = args.title

    def run(self) -> Notification:
        return Notification(self._title, _format_today(self._format))
