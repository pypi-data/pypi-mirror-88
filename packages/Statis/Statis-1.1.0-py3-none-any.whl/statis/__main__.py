"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
import logging
import sys
from typing import Callable, Dict, List, NoReturn, Optional, Union

from statis import cli, search
from statis import notification as nf
from statis.monitor import Monitor, PollingMonitor
from statis.monitor import Threshold, ThresholdUnitError
from statis.notifier import Notifier, NotifierError

SendCallback = Callable[[], None]


def main(arg_list: List[str] = None) -> Union[int, NoReturn]:
    """
    Initialize, parse CLI arguments, and run a specified notifier.

    :return: An exit status to terminate the process with
    """
    if arg_list is None:
        arg_list = sys.argv[1:]

    cli.setup_logging()
    args: argparse.Namespace = cli.parse_args(arg_list)

    if args.list:
        _print_notifier_list()
        return 0

    try:
        notifier: Notifier = search.find_notifier(args.module, args.notifier)
    except FileNotFoundError as e:
        logging.error(str(e))
        return 66

    notifier.parse_args(args.notifier_args)
    send_callback: SendCallback = _get_send_callback(notifier, args)

    try:
        if args.monitor is None:
            send_callback()
        else:
            if not isinstance(notifier, Monitor):
                logging.error('This notifier does not support monitoring.')
                return 2

            threshold: Optional[Threshold] = args.monitor or None
            _run_monitor(notifier, send_callback, threshold, args.polling_rate)
    except NotifierError as e:
        logging.error('Failed to run notifier: %s', e)
        return 1
    except ThresholdUnitError as e:
        logging.error(str(e))
        return 65

    return 0


def _run_monitor(monitor: Monitor, event_callback: SendCallback,
                 threshold: Optional[Threshold],
                 polling_rate: Optional[float]) -> NoReturn:
    """
    Set up the given monitor and run its monitoring implementation.

    :param monitor: The :class:`Monitor` to set up and run
    :param event_callback: A callback to run upon monitoring events
    :param threshold: A threshold at which to invoke the callback or
                      `None` to do so on all changes to the measure
    :param polling_rate: A custom polling rate to monitor with; only
                         relevant for polling-based implementations

    :raises ThresholdUnitError: if the threshold unit is unsupported
    :raises NotifierError: if the callback's notifier failed to run
    """
    if polling_rate is not None:
        if isinstance(monitor, PollingMonitor):
            monitor.polling_rate = polling_rate
        else:
            logging.warning('This monitor does not employ polling, '
                            'ignoring rate argument.')

    monitor.configure_monitor(event_callback, threshold)

    if threshold is None:
        print('No threshold supplied; notifying on all changes...')
    else:
        print(f'Monitoring and notifying at {threshold.type.value} '
              f'{threshold.value} {threshold.unit}...')

    monitor.monitor()


def _get_send_callback(notifier: Notifier,
                       args: argparse.Namespace) -> SendCallback:
    """
    Return a callback function which runs the given notifier.

    The primary use for this is monitors, since they run indefinitely
    and can't simply return a notification instance. The sending also
    requires certain argument values, which the callback already gets
    from this function's scope.

    :param notifier: The notifier to run
    :param args: A namespace holding all CLI arguments
    :return: A callback function which runs the given notifier
    """

    def send_notification() -> None:
        """
        Run the notifier and send its returned notification.

        :raises NotifierError: if the notifier failed to run
        """
        notification: nf.Notification = notifier.run()
        replace_id: int = nf.id_from_string(args.module + args.notifier)
        nf.send(notification, args.timeout, args.urgency, replace_id)

    return send_notification


def _print_notifier_list() -> None:
    """
    Print a list of all available notifiers grouped by module.
    """
    notifiers_by_module: Dict[str, List[str]] = search.list_all()
    for module in notifiers_by_module:
        print(module)
        for notifier in notifiers_by_module[module]:
            print(f' * {notifier}')


if __name__ == '__main__':
    sys.exit(main())
