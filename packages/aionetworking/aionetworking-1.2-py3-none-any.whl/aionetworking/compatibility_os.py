import signal
import asyncio
import os
import platform
import sys
from functools import partial
try:
    import psutil
except ImportError:
    psutil = None

from aionetworking.types.logging import LoggerType


from typing import Callable
try:
    from systemd import daemon
    from systemd import journal

    def send_to_journal(*args, logger: LoggerType=None, **kwargs):
        if logger:
           logger.info(args[0])
        journal.send(*args, **kwargs)

    def send_ready():
        daemon.notify('READY=1')

    def send_status(status: str):
        daemon.notify(f'STATUS={status}')

    def send_stopping():
        daemon.notify('STOPPING=1')

    def send_reloading():
       daemon.notify('RELOADING=1')
except ImportError:
    def send_to_journal(*args, **kwargs): ...

    def send_ready():
        pass

    def send_status(status: str):
        pass

    def send_stopping():
        pass

    def send_reloading():
        pass


def loop_on_signal(signum: int, callback: Callable, logger: LoggerType = None):
    if logger:
        logger.info('Signal %s received', signum)
    callback()
    if logger:
        logger.info('Completed callback for signal %s', signum)
    if os.name != 'nt' and any(s == signum for s in (signal.SIGINT, signal.SIGTERM)):
        loop = asyncio.get_event_loop()
        loop.remove_signal_handler(signal.SIGINT)
        loop.remove_signal_handler(signal.SIGTERM)


def loop_on_user1_signal(callback: Callable, logger: LoggerType = None):
    if os.name == 'posix':
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGUSR1, partial(loop_on_signal, signal.SIGUSR1, callback, logger))


def loop_on_close_signal(callback: Callable, logger: LoggerType = None):
    if os.name == 'posix':
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, partial(loop_on_signal, signal.SIGTERM, callback, logger))
        loop.add_signal_handler(signal.SIGINT, partial(loop_on_signal, signal.SIGINT, callback, logger))


def loop_remove_signals():
    if os.name == 'posix':
        loop = asyncio.get_event_loop()
        loop.remove_signal_handler(signal.SIGTERM)
        loop.remove_signal_handler(signal.SIGINT)
        loop.remove_signal_handler(signal.SIGUSR1)


def send_notify_start_signal(pid: int):
    if os.name == 'posix':
        os.kill(pid, signal.SIGUSR2)


def is_wsl() -> bool:
    return os.name == 'posix' and 'microsoft' in platform.uname().release.lower()


def is_aix() -> bool:
    return sys.platform.startswith("aix")


if os.name == 'posix':
    import pamela
    authentication_type = 'PAM'

    def authenticate(username: str, password: str, pam_service: str = 'sftplogin', **kwargs) -> bool:
        try:
            pamela.authenticate(username, password, pam_service)
            return True
        except pamela.PAMError:
            return False
elif os.name == 'nt':
    import pywintypes
    import win32security
    import win32con

    authentication_type = 'WINDOWS'

    def authenticate(username: str, password: str, domain: str = '.', logon_type=win32con.LOGON32_LOGON_BATCH,
                     logon_provider=win32con.LOGON32_PROVIDER_DEFAULT, **kwargs) -> bool:
        try:
            win32security.LogonUser(username, domain, password, logon_type, logon_provider)
            return True
        except pywintypes.error:
            return False


def windows_and_is_administrator() -> bool:
    if not os.name == 'nt':
        return False
    from win32com.shell import shell
    return shell.IsUserAnAdmin()


def has_ip_address(ip: str) -> bool:
    interfaces = psutil.net_if_addrs().values()
    for i in interfaces:
        if any(a.address == ip for a in i):
            return True
    return False


def is_mac_os() -> bool:
    return sys.platform == 'darwin'
