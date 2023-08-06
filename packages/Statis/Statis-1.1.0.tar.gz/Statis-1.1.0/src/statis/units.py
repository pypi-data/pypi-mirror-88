"""
Utilities for conversion between measurement units.

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

from typing import Tuple

MEM_UNIT_PREFIXES: Tuple[str, ...] = ('k', 'm', 'g', 't', 'p', 'e', 'z', 'y')


def bytes_to_unit(no_of_bytes: int, target_unit: str) -> float:
    """
    Convert the given no. of bytes to an SI- or IEC-prefixed unit.

    * SI prefixes (kB, MB, etc.) are decimal, i.e. powers of 1000,
      meaning 1 MB = 1000 kB = 1000000 Bytes
    * IEC prefixes (KiB, MiB, etc.) are binary, i.e. powers of 2,
      meaning 1 MiB = 1024 KiB = 1048576 Bytes

    Examples:
      >>> bytes_to_unit(1_000_000, 'kB')
      1000.0
      >>> bytes_to_unit(1_000_000, 'KiB')
      976.5625

    See: https://en.wikipedia.org/wiki/Binary_prefix#Definitions

    :param no_of_bytes: No. of bytes to convert to a prefixed unit
    :param target_unit: The SI- or IEC-prefixed unit to convert to
    :return: The converted value

    :raises ValueError: if the given target unit is empty/invalid
    """
    target_unit_lc = target_unit.lower()

    if (not target_unit_lc.startswith(MEM_UNIT_PREFIXES)
            or target_unit_lc[1:] not in ('b', 'ib')):
        raise ValueError(f'"{target_unit}" is not a valid memory unit.')

    factor: int = 1024 if target_unit_lc.endswith('ib') else 1000
    order: int = MEM_UNIT_PREFIXES.index(target_unit_lc[0]) + 1
    return no_of_bytes / (factor ** order)


def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert the given temperature from Celsius to Fahrenheit.

    :param celsius: A temperature in Celsius to convert
    :return: The temperature in Fahrenheit
    """
    return celsius * 9 / 5 + 32
