"""
A libnotify-compliant notification and utilities for sending it.

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import logging
import shutil
import subprocess
import zlib
from dataclasses import dataclass
from enum import Enum
from typing import List


class Urgency(Enum):
    """
    Urgency levels to mark a notification's importance with.

    See: https://developer.gnome.org/notification-spec/#urgency-levels
    """

    LOW = 'low'
    NORMAL = 'normal'
    CRITICAL = 'critical'


class Category(Enum):
    """
    Categories assignable to a notification to indicate its type.

    Most system status notifications should probably use 'device', but
    there may be cases where a different category makes sense, such as
    custom notifiers that are triggered by external scripts.

    See: https://developer.gnome.org/notification-spec/#categories
    """

    DEVICE = 'device'
    DEVICE_ADDED = 'device.added'
    DEVICE_ERROR = 'device.error'
    DEVICE_REMOVED = 'device.removed'

    EMAIL = 'email'
    EMAIL_ARRIVED = 'email.arrived'
    EMAIL_BOUNCED = 'email.bounced'

    IM = 'im'
    IM_ERROR = 'im.error'
    IM_RECEIVED = 'im.received'

    NETWORK = 'network'
    NETWORK_CONNECTED = 'network.connected'
    NETWORK_DISCONNECTED = 'network.disconnected'
    NETWORK_ERROR = 'network.error'

    PRESENCE = 'presence'
    PRESENCE_OFFLINE = 'presence.offline'
    PRESENCE_ONLINE = 'presence.online'

    TRANSFER = 'transfer'
    TRANSFER_COMPLETE = 'transfer.complete'
    TRANSFER_ERROR = 'transfer.error'


@dataclass
class Notification:
    """
    A notification comprised of attributes from the `libnotify spec`_.

    Some attributes from the spec are purposefully left out, as they
    are the same across notifiers or user-defined (e.g. the timeout).

    .. _`libnotify spec`: https://developer.gnome.org/notification-spec/
    """

    title: str
    content: str
    icon: str = ''

    category: Category = Category.DEVICE

    # Dunst-specific
    action: str = ''


def send(notification: Notification, timeout: float,
         urgency: str, replace_id: int) -> None:
    """
    Send a notification using Dunst (if available) or `notify-send`.

    :param notification: The notification to send
    :param timeout: Seconds after which to expire the notification
    :param urgency: An urgency level to mark the notification with
    :param replace_id: A replace ID unique to this notification type
    """
    timeout_ms: int = int(timeout * 1000)
    args: List[str] = [notification.title, notification.content,
                       '-i', notification.icon, '-t', str(timeout_ms),
                       '-u', urgency, '-a', 'Statis']

    if shutil.which('dunstify') and 'dunst' in _get_active_daemon():
        command = 'dunstify'
        args.append(f'--replace={replace_id}')
        args.append(f'--hints=string:category:{notification.category.value}')

        if notification.action:
            args.append(f'--action={notification.action}')
    else:
        command = 'notify-send'
        args.extend(['-c', notification.category.value])

    logging.info('Running "%s" to send notification: "%s" / "%s"',
                 command, notification.title, notification.content)
    subprocess.run([command] + args, check=True)


def id_from_string(string: str) -> int:
    """
    Create a notification ID unique to the given string.

    It is used to replace a previous notification of the same ID and
    must fit in a 32-bit integer. Since this use case doesn't require
    cryptographic security, the ID is just the first 6 digits of the
    string's CRC32 digest, which should be sufficiently unique.

    :param string: The string to create a notification ID from
    :return: A 6-digit ID unique to the given string
    """
    return int(str(zlib.crc32(string.lower().encode()))[:6])


def _get_active_daemon() -> str:
    """
    Retrieve details on the active notification server over D-Bus.

    This is done via the `GetServerInformation` message that must be
    supported by any `spec`_-compliant notification server connected
    to the `org.freedesktop.Notifications` bus.

    .. _`spec`: https://developer.gnome.org/notification-spec/#commands

    :return: A string containing the server name, vendor, and version
    """
    server_info: bytes = subprocess.check_output([
        'dbus-send', '--dest=org.freedesktop.Notifications',
        '--print-reply=literal', '/org/freedesktop/Notifications',
        'org.freedesktop.Notifications.GetServerInformation'
    ])
    return server_info.decode().strip()
