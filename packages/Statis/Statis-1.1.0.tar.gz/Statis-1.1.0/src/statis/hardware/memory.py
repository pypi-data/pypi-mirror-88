"""
Wrappers around `psutil` for retrieving memory information.

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import psutil


def total() -> int:
    """
    Return the total installed memory in bytes.

    :return: The total installed memory in bytes
    """
    return psutil.virtual_memory().total


def available() -> int:
    """
    Return the currently available memory in bytes.

    :return: The currently available memory in bytes
    """
    return psutil.virtual_memory().available


def used() -> int:
    """
    Return the currently used memory in bytes.

    In this case, this is the (total - available) memory, i.e.
    the one that is currently in use and cannot be reallocated
    without swapping.

    See https://unix.stackexchange.com/a/550855 for more info.

    :return: The currently used memory in bytes
    """
    return psutil.virtual_memory().total - psutil.virtual_memory().available


def total_swap() -> int:
    """
    Return the total swap space in bytes.

    :return: The total swap space in bytes
    """
    return psutil.swap_memory().total


def free_swap() -> int:
    """
    Return the currently free swap space in bytes.

    :return: The currently free swap space in bytes
    """
    return psutil.swap_memory().free


def used_swap() -> int:
    """
    Return the currently used swap space in bytes.

    :return: The currently used swap space in bytes
    """
    return psutil.swap_memory().used
