"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
import operator
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, NoReturn, Optional

Comparator = Callable[[float, float], bool]


@dataclass
class Threshold:
    """A threshold to notify at when reached by the current value."""

    class Type(Enum):
        """Possible comparisons between measurement and threshold."""

        EQUAL = '='
        ABOVE = '>'
        BELOW = '<'
        ABOVE_EQ = '>='
        BELOW_EQ = '<='

    value: float
    unit: str
    type: 'Threshold.Type' = Type.ABOVE


class ThresholdUnitError(ValueError):
    """
    Raised if a monitor does not support the given threshold's unit.

    Valid units are defined by :meth:`Monitor.valid_threshold_units`.
    """


COMPARISON_OPS: Dict[Threshold.Type, Comparator] = {
    Threshold.Type.EQUAL: operator.eq,
    Threshold.Type.ABOVE: operator.gt,
    Threshold.Type.BELOW: operator.lt,
    Threshold.Type.ABOVE_EQ: operator.ge,
    Threshold.Type.BELOW_EQ: operator.le,
}


class Monitor(ABC):
    """A mixin for use with :class:`Notifier` to enable monitoring."""

    parser: argparse.ArgumentParser

    def __init__(self) -> None:
        super().__init__()
        self.event_callback: Callable = None
        self.threshold: Optional[Threshold] = None

        self._previous_value: Optional[float] = None

        self.parser.epilog = ('\033[1mMonitoring supported\033[0m\n'
                              '  Valid threshold units: ' +
                              ', '.join(self.valid_threshold_units()))

    def configure_monitor(self, event_callback: Callable,
                          threshold: Optional[Threshold]) -> None:
        if (threshold is not None
                and threshold.unit not in self.valid_threshold_units()):
            raise ThresholdUnitError(f'Threshold unit "{threshold.unit}" '
                                     f'is not supported by this monitor.')

        self.event_callback = event_callback
        self.threshold = threshold

    def check_threshold(self, current_value: float,
                        total_value: Optional[float] = None) -> None:
        """
        Invoke the notification callback if applicable.

        "Applicable" means one of two things here:
          * If *no* threshold is set: The current value has changed
            (in any way) between the last invocation and now.
          * If a threshold is set: The current value has reached it.
            Only a single notification is sent for this event.

        *Note*: If '%' is set as the threshold unit, the comparison
        will be percentage-based and a total value must be supplied.

        :param current_value: The notifier's current measurement
                              (must already be in threshold unit)
        :param total_value: The respective measurement's total value
                            (required if threshold unit may be '%')

        :raises TypeError: if unit is '%' but no total was supplied
        :raises ValueError: if unit is '%' but supplied total was 0
        """
        if self.threshold is None:
            if (self._previous_value is not None
                    and current_value != self._previous_value):
                self.event_callback()

            self._previous_value = current_value
            return

        if self.threshold.unit == '%':
            if total_value is None:
                raise TypeError('Cannot calculate percentage due to '
                                'no total being supplied.')

            try:
                current_value = current_value / total_value * 100
            except ZeroDivisionError as e:
                raise ValueError('Cannot calculate percentage with '
                                 'supplied total of 0.') from e

        compare: Comparator = COMPARISON_OPS[self.threshold.type]
        threshold_reached: bool = compare(current_value, self.threshold.value)
        threshold_reached_with_prev: bool = (self._previous_value is not None
                                             and compare(self._previous_value,
                                                         self.threshold.value))

        if threshold_reached and not threshold_reached_with_prev:
            self.event_callback()

        self._previous_value = current_value

    @abstractmethod
    def monitor(self) -> NoReturn:
        """
        Override to implement monitoring functionality.

        Most likely this means retrieving the notifier's measurement
        and passing it to :meth:`check_threshold`, which compares it
        to the threshold and sends a notification if applicable.

        Monitoring is usually implemented as either an inotify watch
        or a polling loop. The latter is not as efficient, but often
        necessary due to many readings not being exposed by sysfs.

        *Note*: Rather than manually implementing polling loops, any
        monitors using it should inherit from :class:`PollingMonitor`
        and implement logic in :meth:`PollingMonitor.poll`, which is
        automatically run at a set interval.
        """

    @abstractmethod
    def valid_threshold_units(self) -> List[str]:
        """
        Return a list of threshold units supported by this monitor.

        If '%' is included in the list and :meth:`check_threshold` is
        used for threshold comparison, a total must be supplied to it.

        :return: A list of threshold units supported by this monitor
        """


class PollingMonitor(Monitor, ABC):
    """A mixin to be implemented by monitors based on polling."""

    def __init__(self) -> None:
        super().__init__()
        self.polling_rate: float = 5

    def monitor(self) -> NoReturn:
        while True:
            self.poll()
            time.sleep(self.polling_rate)

    @abstractmethod
    def poll(self) -> None:
        """Override to implement monitoring functionality."""
