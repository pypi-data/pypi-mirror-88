"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
from typing import List, Optional

from statis.hardware import cpu
from statis.monitor import PollingMonitor
from statis.notification import Notification
from statis.notifier import Notifier


class Usage(Notifier, PollingMonitor):
    """A notifier for the current total and per-core CPU usage."""

    def __init__(self) -> None:
        super().__init__()

        self._core: Optional[int] = None
        self._core_count: int = cpu.core_count()

    def description(self) -> str:
        return 'Display the current CPU usage in total or for a single core.'

    def add_args(self) -> None:
        self.parser.add_argument('-c', '--core', type=int, metavar='N',
                                 help=f'a CPU core (1-{self._core_count}) '
                                      f'whose usage to display')

    def handle_args(self, args: argparse.Namespace) -> None:
        if args.core is not None and not 1 <= args.core <= self._core_count:
            self.parser.error(f'Core number must be between '
                              f'1 and {self._core_count}.')

        self._core = args.core

    def run(self) -> Notification:
        title: str = 'CPU Usage'
        if self._core is not None:
            title += f' (Core {self._core})'

        cpu_usage: float = cpu.usage(core_num=self._core)
        return Notification(title, f'{cpu_usage} %')

    def poll(self) -> None:
        self.check_threshold(cpu.usage(core_num=self._core), 100)

    def valid_threshold_units(self) -> List[str]:
        return ['%']


class Frequency(Notifier, PollingMonitor):
    """A notifier for the current CPU frequency."""

    def description(self) -> str:
        return 'Display the current CPU frequency.'

    def run(self) -> Notification:
        frequency: float = cpu.frequency()
        if frequency >= 1000:
            content = f'{frequency / 1000:.2f} GHz'
        else:
            content = f'{frequency:.1f} MHz'

        return Notification('CPU Frequency', content)

    def poll(self) -> None:
        frequency: float = cpu.frequency()
        if self.threshold is not None and self.threshold.unit == 'GHz':
            frequency = frequency / 1000

        self.check_threshold(frequency, cpu.max_frequency())

    def valid_threshold_units(self) -> List[str]:
        return ['MHz', 'GHz', '%']


class Governor(Notifier):
    """A notifier for the active CPU governor."""

    def description(self) -> str:
        return 'Display the currently active governor on CPU 0.'

    def run(self) -> Notification:
        return Notification('CPU Governor', cpu.governor())
