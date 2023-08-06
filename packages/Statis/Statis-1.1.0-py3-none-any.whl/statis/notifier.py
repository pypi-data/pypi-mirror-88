"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
from abc import ABC, abstractmethod
from typing import List

from statis.notification import Notification


class Notifier(ABC):
    """
    A base class to be implemented by individual notifiers.

    Any notifier must extend this class (or another class doing so,
    such as helpers with predefined arguments) to be discoverable.
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description=self.description(),
            formatter_class=argparse.RawTextHelpFormatter)
        super().__init__()

    def set_command_name(self, cmd_name: str) -> None:
        """
        Set the command name to be shown in the notifier's usage hint.

        By default, this would only be the program name rather than the
        actual notifier. Since it is invoked dynamically, this needs to
        be set manually in order for the usage hint to be correct.

        :param cmd_name: The command name to be shown in the usage hint
        """
        self.parser.prog = cmd_name

    # pylint: disable=no-self-use
    def description(self) -> str:
        """
        Override to set a description for the notifier's help message.

        :return: A description for the notifier's help message
        """
        return 'No description available'

    def parse_args(self, cmd_args: List[str]) -> None:
        """
        Process any CLI arguments passed to the notifier's subcommand.

        :param cmd_args: A list of arguments passed to the notifier
        """
        self.add_args()
        args: argparse.Namespace = self.parser.parse_args(cmd_args)
        self.handle_args(args)

    def add_args(self) -> None:
        """
        Override to add custom CLI arguments to the notifier's parser.
        """

    def handle_args(self, args: argparse.Namespace) -> None:
        """
        Override to validate and assign the previously added arguments.

        :param args: A namespace holding all parsed CLI arguments
        """

    @abstractmethod
    def run(self) -> Notification:
        """
        Build and return the notification to be shown by this notifier.

        :return: The notification to be shown by this notifier
        :raises NotifierError: if no notification could be built
        """


class NotifierError(RuntimeError):
    """Raised if a notifier failed to build its notification."""
