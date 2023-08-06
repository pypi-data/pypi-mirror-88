from os import path
from sys import platform

from pynotifier import Notification


__all__ = ['WorkNotification', ]


LINUX_NAMES = ('linux', 'linux2', )
OSX_NAMES = ('darwin', )
WINDOWS_NAMES = ('win32', )

WINDOWS = 'windows'
LINUX = 'linux'
OSX = 'osx'


class WorkNotification:

    def __init__(self):
        if platform in WINDOWS_NAMES:
            self.operation_system = WINDOWS
        elif platform in OSX_NAMES:
            self.operation_system = OSX
        else:
            self.operation_system = LINUX

        self.title = 'Work scheduler'
        cur_directory = path.dirname(__file__)
        self.linux_icon = path.join(cur_directory, 'media', 'icon.png')


    def notify(self, body: str) -> None:
        notify_mapper = {
            WINDOWS: self._notify_windows,
            LINUX: self._notify_linux,
            OSX: self._notify_osx
        }
        notify_mapper[self.operation_system](body)

    def _notify_linux(self, text):
        """
            Icon must have .png extension
        """
        try:
            Notification(
                title=self.title,
                description=text,
                icon_path=self.linux_icon,
                duration=5 * 60,
                urgency=Notification.URGENCY_LOW
            ).send()
        except:
            raise SystemError(f'You must have `send-notify` library on your linux machine')

    def _notify_osx(self, text):
        pass

    def _notify_windows(self, text):
        """
            Icon must have .ico extension
        """
        pass
