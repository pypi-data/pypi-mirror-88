"""
Utilities and `psutil`-wrappers for retrieving CPU information.

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import pathlib
from typing import List, Optional, Union

import psutil


def core_count() -> int:
    """
    Return the total number of logical CPU cores.

    :return: The total number of logical CPU cores
    """
    return psutil.cpu_count()


def usage(interval: float = 0.2, core_num: Optional[int] = None) -> float:
    """
    Return the current CPU usage in percent.

    The only way to obtain the "current" CPU usage on *nix is to take
    at least two subsequent readings of the total CPU time and compare
    the elapsed times before and after the measurement interval.

    Thus, this function call is *blocking* for the specified interval.
    A higher one may result in better accuracy but also a longer delay
    before - in this context - a notification can be shown.

    :param interval: The interval between both CPU time measurements
                     (must be greater than 0, default: 0.2)
    :param core_num: A specific core (1-indexed) whose usage to get
    :return: The current CPU usage in percent
    """
    assert interval > 0 and (core_num is None or core_num > 0)

    per_core: bool = core_num is not None
    percent: Union[float, List[float]] = psutil.cpu_percent(interval=interval,
                                                            percpu=per_core)
    return percent[core_num - 1] if per_core else percent


def frequency() -> float:
    """
    Return the current CPU frequency in MHz.

    :return: The current CPU frequency in MHz
    """
    return psutil.cpu_freq().current


def max_frequency() -> float:
    """
    Return the maximum CPU frequency in MHz.

    :return: The maximum CPU frequency in MHz
    """
    return psutil.cpu_freq().max


def governor() -> str:
    """
    Return the currently active CPU governor.

    This only returns the governor for CPU 0, but in most practical
    applications, all cores will (probably) use the same governor.

    :return: The currently active CPU governor
    """
    cpu0_governor: pathlib.Path = pathlib.Path('/sys/devices/system/cpu/cpu0/'
                                               'cpufreq/scaling_governor')
    return cpu0_governor.read_text()
