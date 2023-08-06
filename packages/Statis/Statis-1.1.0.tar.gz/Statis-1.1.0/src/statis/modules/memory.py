"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

from typing import List, Union

from statis import units
from statis.hardware import memory
from statis.monitor import PollingMonitor
from statis.notification import Notification
from statis.notifier_types.memory import MemoryNotifier

THRESHOLD_UNITS: List[str] = ['MB', 'MiB', 'GB', 'GiB', 'TB', 'TiB', '%']


class Used(MemoryNotifier, PollingMonitor):
    """A notifier for the currently used memory."""

    def description(self) -> str:
        return 'Display the current memory usage.'

    def run(self) -> Notification:
        content: str = self._format_content(memory.used(),
                                            memory.total())
        return Notification('Used Memory', content)

    def poll(self) -> None:
        used_mem: Union[int, float] = memory.used()
        if self.threshold is not None and self.threshold.unit != '%':
            used_mem = units.bytes_to_unit(used_mem, self.threshold.unit)

        self.check_threshold(used_mem, memory.total())

    def valid_threshold_units(self) -> List[str]:
        return THRESHOLD_UNITS


class Free(MemoryNotifier):
    """A notifier for the currently available memory."""

    def description(self) -> str:
        return 'Display the currently available memory.'

    def run(self) -> Notification:
        content: str = self._format_content(memory.available(),
                                            memory.total())
        return Notification('Available Memory', content)


class UsedSwap(MemoryNotifier, PollingMonitor):
    """A notifier for the currently used swap space."""

    def description(self) -> str:
        return 'Display the current swap space usage.'

    def run(self) -> Notification:
        content: str = self._format_content(memory.used_swap(),
                                            memory.total_swap())
        return Notification('Used Swap', content)

    def poll(self) -> None:
        used_swap: Union[int, float] = memory.used_swap()
        if self.threshold is not None and self.threshold.unit != '%':
            used_swap = units.bytes_to_unit(used_swap, self.threshold.unit)

        self.check_threshold(used_swap, memory.total_swap())

    def valid_threshold_units(self) -> List[str]:
        return THRESHOLD_UNITS


class FreeSwap(MemoryNotifier):
    """A notifier for the currently free swap space."""

    def description(self) -> str:
        return 'Display the currently free swap space.'

    def run(self) -> Notification:
        content: str = self._format_content(memory.free_swap(),
                                            memory.total_swap())
        return Notification('Free Swap', content)
