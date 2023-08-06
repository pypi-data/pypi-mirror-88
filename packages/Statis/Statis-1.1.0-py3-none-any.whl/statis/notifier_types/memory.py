"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
from abc import ABC
from typing import List

from statis import units
from statis.notifier import Notifier, NotifierError


class MemoryNotifier(Notifier, ABC):
    """A base class for notifiers that display memory values."""

    def __init__(self) -> None:
        super().__init__()

        self._mem_unit: str = 'GB'
        self._show_total: bool = False

        self.parser.add_argument('-u', '--unit', metavar='str', default='GB',
                                 help='an SI/IEC unit to use or "%%" '
                                      'to show a percentage')
        self.parser.add_argument('-t', '--show-total', action='store_true',
                                 help='include the total (ignored if '
                                      'percentage is shown)')

    def parse_args(self, cmd_args: List[str]) -> None:
        self.add_args()

        args: argparse.Namespace = self.parser.parse_args(cmd_args)
        self._mem_unit = args.unit
        self._show_total = args.show_total

        self.handle_args(args)

    def _format_content(self, current_bytes: int, total_bytes: int) -> str:
        """
        Format a memory display to be used in the notification.

        The resulting string may have one of the following formats,
        depending on which arguments were supplied to the notifier:

          * "<current> <unit>" by default
          * "<current> / <total> <unit>" if the total flag is set
          * "<percentage>" if a percent sign is given as the unit

        :param current_bytes: The current memory amount in bytes
        :param total_bytes: The total memory amount in bytes
        :return: A friendly memory display string

        :raises NotifierError: if the set unit is empty or invalid
        """
        if self._mem_unit == '%':
            return f'{current_bytes / total_bytes * 100:.1f} %'

        try:
            current: float = units.bytes_to_unit(current_bytes, self._mem_unit)
            content: str = f'{current:.2f}'

            if self._show_total:
                total: float = units.bytes_to_unit(total_bytes, self._mem_unit)
                content += f' / {total:.2f}'
        except ValueError as e:
            raise NotifierError(str(e))

        return f'{content} {self._mem_unit}'
