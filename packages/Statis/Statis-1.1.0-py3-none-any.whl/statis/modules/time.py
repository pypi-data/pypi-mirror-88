"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
from datetime import datetime
from typing import Optional

import pytz

from statis.notification import Notification
from statis.notifier import Notifier


class Time(Notifier):
    """A notifier for the current time (in a given timezone)."""

    def __init__(self) -> None:
        super().__init__()

        self._use_12h_format: bool = False
        self._tz_name: Optional[str] = None

    def description(self) -> str:
        return 'Display the current time.'

    def add_args(self) -> None:
        self.parser.add_argument('--12', action='store_true', dest='use_12h',
                                 help='use 12-hour time notation (am/pm)')
        self.parser.add_argument('-t', '--timezone', metavar='TZ',
                                 help='a timezone to display the time in\n'
                                      '(tz database name)')

        self.parser.epilog = ('list of tz database timezones:\n'
                              '  https://en.wikipedia.org/wiki/'
                              'List_of_tz_database_time_zones')

    def handle_args(self, args: argparse.Namespace) -> None:
        self._use_12h_format = args.use_12h
        self._tz_name = args.timezone

        if (self._tz_name is not None
                and self._tz_name not in pytz.all_timezones):
            self.parser.error('The given timezone does not exist.')

    def run(self) -> Notification:
        title: str = 'Time'
        timezone: Optional[datetime.tzinfo] = None

        if self._tz_name is not None:
            title += f' ({self._tz_name.split("/")[-1].replace("_", " ")})'
            timezone = pytz.timezone(self._tz_name)

        current_time: datetime.time = datetime.now(timezone).time()
        time_format: str = '%I:%M %p' if self._use_12h_format else '%H:%M'

        return Notification(title, current_time.strftime(time_format))
