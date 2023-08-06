import asyncio
from collections import ChainMap
from ipaddress import AddressValueError
import builtins
import operator
import os
import re
import signal
import time
import itertools
import sys
import socket
import tempfile
from aiofiles.os import wrap
from aionetworking.compatibility import py38, net_supernet_of, WindowsProactorEventLoopPolicy, WindowsSelectorEventLoopPolicy
from aionetworking.compatibility_os import is_wsl, is_aix
from dataclasses import dataclass, fields, MISSING
from functools import wraps

from .compatibility import Protocol
from pathlib import Path
from typing import Sequence, Callable, List, AnyStr, Tuple, Union, AsyncGenerator, Any, TYPE_CHECKING, Optional, Iterable
from ipaddress import IPv4Network, IPv6Network, IPv4Address, IPv6Address

try:
    import psutil
    supports_system_info = True
except ImportError:
    psutil = None
    supports_system_info = False


str_to_list = re.compile(r"^\s+|\s*,\s*|\s+$")


def better_file_not_found_error(*files: Union[str, Path], purpose: str = None):
    if purpose:
        additional = f'required for {purpose } '
    else:
        additional = ''
    for i, path in enumerate(files):
        path = Path(path)
        if not path.exists():
            return f'Path {path} {additional}was not found'
    return f'Unknown file {additional}was not found'


###Coroutines###
makedirs = wrap(os.makedirs)
    
    
async def time_coro(coro):
    start_time = time.time()
    await coro
    return time.time() - start_time


"""
async def benchmark(async_func: Callable, *args, num_times: int = 5, quiet: bool = False, cleanup: Callable = None,
                    cleanup_args=(), num_items: int = None, num_bytes: int = None, ignore_first: bool = True, **kwargs):
    times = []
    if not quiet:
        print("Running", async_func.__name__)
    total = 0
    if ignore_first:
        await time_coro(async_func(*args, **kwargs))
        if cleanup:
            await cleanup(*cleanup_args)
    for _ in range(0, num_times):
        time_taken = await time_coro(async_func(*args, **kwargs))
        if cleanup:
            await cleanup(*cleanup_args)
        times.append(str(time_taken))
        total += time_taken
        if not quiet:
            print(time_taken)
    average = total / num_times
    if not quiet:
        print("Average time taken:", average)
        if num_items:
            average_per_item = average / num_items
            items_per_second = 1 / average_per_item
            print('Num Items:', num_items)
            print("Average per item:", average_per_item)
            print("Items per second:", items_per_second)
            if num_bytes:
                print("Bytes per second:", (num_bytes / average))
                times = '\t'.join(times)
                print(f"{async_func.__name__}\t{num_bytes}\t{num_items}\t{times}")

"""
###Dataclasses###

def dataclass_getstate(self):
    state = {}
    f = fields(self)
    for field in f:
        name = field.name
        if field.init:
            try:
                value = getattr(self, field.name)
                if field.default == MISSING and field.default_factory == MISSING:
                    state[name] = value
                elif field.default != MISSING and value != field.default:
                    if field.metadata.get('pickle', True):
                        state[name] = value
                elif field.default_factory != MISSING:
                    if field.metadata.get('pickle', False):
                        state[name] = value
            except AttributeError:
                pass
    return state


def dataclass_setstate(self, state):
    self.__dict__.update(self.__class__(**state).__dict__)


###Typing###

class EmptyProtocol(Protocol):
    pass


def inherit_on_type_checking_only(arg):
    """Decorator for protocols/ABC classes who's methods can be used for
    type checking on subclasses but are not available at runtime.
    Used to add type hints for dynamic attributes (__getattr__, etc)
    """
    if TYPE_CHECKING:
        return arg
    return EmptyProtocol


###Async Generators###

async def aone(generator: AsyncGenerator) -> Any:
    item = await generator.__anext__()
    await generator.aclose()
    return item


async def anext(generator: AsyncGenerator) -> Any:
    return await generator.__anext__()


async def alist(generator: AsyncGenerator) -> List[Any]:
    return [i async for i in generator]


###Asyncio###

def run_in_loop(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        return asyncio.run(f(*args, **kwds))

    return wrapper


def set_proactor_loop_policy_windows() -> None:
    asyncio.set_event_loop_policy(WindowsProactorEventLoopPolicy())


def set_selector_loop_policy_windows() -> None:
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


def set_selector_loop_policy_posix() -> None:
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())


def set_uvloop_policy_posix() -> None:
    import uvloop
    uvloop.install()


class InvalidLoopNameException(BaseException):
    pass


def set_loop_policy(posix_loop_type: str = None, windows_loop_type: str = None) -> None:
    if os.name == 'posix':
        if posix_loop_type == 'selector':
            set_selector_loop_policy_posix()
        elif posix_loop_type == 'uvloop':
            set_uvloop_policy_posix()
        else:
            raise InvalidLoopNameException(
                f'{posix_loop_type} is not a valid loop name. Choose either selector or uvloop')
    elif os.name == 'nt':
        if windows_loop_type == 'selector':
            set_selector_loop_policy_windows()
        elif windows_loop_type == 'proactor':
            set_proactor_loop_policy_windows()
        else:
            raise InvalidLoopNameException(
                f'{posix_loop_type} is not a valid loop name. Choose either proactor or selector')


###Pipes###

_mmap_counter = itertools.count()


def arbitrary_address(family, future_pid=False) -> Union[Tuple[str, int], Path]:
    if family == 'AF_INET':
        return 'localhost', 0
    if family == 'AF_UNIX':
        return Path(tempfile.mktemp(prefix='listener-', dir=tempfile.mkdtemp(prefix='pymp-')))
    if family == 'AF_PIPE':
        pid = '{pid}' if future_pid else os.getpid()
        return Path(tempfile.mktemp(prefix=r'\\.\pipe\pyc-%d-%d-' %
                               (pid, next(_mmap_counter)), dir=""))
    raise ValueError('unrecognized family')


def unix_address() -> Path:
    return arbitrary_address('AF_UNIX')


def pipe_address() -> Path:
    return arbitrary_address('AF_PIPE')


def pipe_address_by_os() -> Path:
    if hasattr(socket, 'AF_UNIX'):
        return unix_address()
    if sys.platform == 'win32':
        return pipe_address()
    OSError("Neither AF_UNIX nor Named Pipe is supported on this platform")


###Networking###

def hostname_or_ip(host: str):
    if os.name == 'nt':
        if host == '127.0.0.1':
            return 'localhost'
        elif host == '::1':
            return 'ip6-localhost'
    try:
        return socket.gethostbyaddr(host)[0]
    except socket.herror:
        return host


def addr_tuple_to_str(addr: Sequence):
    return ':'.join(str(a) for a in addr)


def addr_str_to_tuple(addr: AnyStr):
    addr, port = addr.split(':')
    return addr, int(port)


def ipv4_or_ipv6(address: Union[str, IPv4Address, IPv6Address]):
    try:
        return IPv4Address(address)
    except AddressValueError:
        return IPv6Address(address)


class IPNetwork:
    ip_network: Union[IPv4Network, IPv6Network] = None
    hostname: str = None
    is_ipv6: bool = False

    def __init__(self, network: Union[str, IPv4Network, IPv6Network]):
        if isinstance(network, IPv4Network):
            self.ip_network = network
        elif isinstance(network, IPv6Network):
            self.ip_network = network
            self.is_ipv6 = True
        else:
            try:
                self.ip_network = IPv4Network(network)
            except AddressValueError:
                try:
                    self.ip_network = IPv6Network(network)
                    self.is_ipv6 = True
                except AddressValueError:
                    if network:
                        self.hostname = network
                    else:
                        AddressValueError('IP Address, Network Or Hostname must be given')

    def __eq__(self, other):
        if self.ip_network:
            return self.ip_network == other.ip_network
        return self.hostname == other.hostname

    def supernet_of(self, network: Union[IPv4Network, IPv6Network], hostname: str):
        if self.ip_network:
            return net_supernet_of(self.ip_network, network)
        return hostname == self.hostname


def supernet_of(network: Union[str, IPNetwork, IPv4Network, IPv6Network], hostname: str, networks: Sequence[IPNetwork]):
    if not isinstance(network, IPNetwork):
        network = IPNetwork(network)
    if network.is_ipv6:
        networks = filter(lambda n: n.is_ipv6, networks)
    else:
        networks = filter(lambda n: not n.is_ipv6, networks)
    return any(n.supernet_of(network.ip_network, hostname) for n in networks)


def port_from_out(out: str) -> int:
    return int(re.search(r'[1-6][0-9]{3,4}', out)[0])


def wait_on_capsys(capsys) -> Tuple[str, int]:
    out = None
    while not out:
        out = capsys.readouterr().out
        if not out:
            time.sleep(0.1)
    port = port_from_out(out)
    return out, port


def raise_signal(signal_num: int, pid: int = None) -> None:
    num_times = 3 if os.name == 'nt' else 1
    if not pid and py38:
        for i in range(0, num_times):
            signal.raise_signal(signal_num)
    else:
        pid = pid or os.getpid()
        for i in range(0, num_times):
            os.kill(pid, signal_num)


def wait_server_started_raise_signal(signal_num: int, host: str, capsys, pid: int = None) -> Tuple[str, int]:
    out, port = wait_on_capsys(capsys)
    assert is_listening_on((host, port), pid=pid)
    raise_signal(signal_num, pid=pid)
    return out, port


def modify_config_file(tmp_config_file, old_host, new_host):
    with open(str(tmp_config_file), "rt") as f:
        data = f.read()
        data = data.replace(old_host, new_host)
    with open(str(tmp_config_file), 'wt') as f:
        f.write(data)


def assert_reload_ok(signal_num: int, host: str, new_host: str, tmp_config_file: Path, capsys) -> Tuple[str, int]:
    out, port = wait_on_capsys(capsys)
    assert is_listening_on((host, port))
    modify_config_file(tmp_config_file, host, new_host)
    raise_signal(signal_num)
    out, new_port = wait_on_capsys(capsys)
    assert not is_listening_on((host, port))
    assert is_listening_on((new_host, new_port))
    raise_signal(signal.SIGINT)
    return out, new_port


def get_ip_port(host: str, transport) -> Tuple[str, int]:
    network = IPNetwork(host)
    if network.is_ipv6:
        actual_ip, actual_port, flowinfo, scope_id = transport.get_extra_info('sockname')
    else:
        actual_ip, actual_port = transport.get_extra_info('sockname')
    return actual_ip, actual_port


###System###


def _process_by_id(pid: int):
    return [p for p in psutil.process_iter() if p.pid == pid][0]


def is_listening_on(addr: Tuple[str, int], kind: str = 'inet', pid: int = None) -> bool:
    if psutil and not is_wsl() and not is_aix():
        pid = pid or os.getpid()
        process = _process_by_id(pid)
        connections = process.connections(kind=kind)
        return any(
            conn.laddr == addr and any(status == conn.status for status in (psutil.CONN_LISTEN, psutil.CONN_NONE)) for
            conn in connections)
    else:
        import subprocess
        process = subprocess.run(f'nc -z {addr[0]} {addr[1]}'.split())
        return process.returncode == 0


class SystemInfo:
    @property
    def memory(self):
        try:
            return psutil.Process(os.getpid()).memory_info()[0]/2.**30
        except NameError:
            return "Unknown"

    @property
    def cpu(self):
        try:
            return psutil.Process(os.getpid()).cpu_percent()
        except NameError:
            return "Unknown"


###Misc###

@dataclass
class CallableFromString(Callable):
    _strings_to_callables = {}
    callable: Callable

    def __post_init__(self):
        self.callable = self.adapt_callable(self.callable)

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

    def adapt_callable(self, v: Union[str, Callable]):
        if isinstance(v, str):
            try:
                return self._strings_to_callables[v]
            except KeyError:
                raise TypeError(f"{v} not found")
        if v not in self._strings_to_callables.values():
            name = self.__class__.__name__
            raise TypeError(f"{v} not a valid {name}")
        return v


class Builtin(CallableFromString):
    _strings_to_callables = ChainMap(builtins.__dict__, {'istr': str})


def in_(a, b) -> bool:
    return a in b


class Operator(CallableFromString):
    _strings_to_callables = {
        '=': operator.eq,
        '==': operator.eq,
        'eq': operator.eq,
        '<': operator.lt,
        'lt': operator.lt,
        '<=': operator.le,
        'lte': operator.le,
        '!<': operator.ne,
        'ne': operator.ne,
        '>': operator.gt,
        'gt': operator.gt,
        '>=': operator.ge,
        'ge': operator.ge,
        'in': in_,
        'contains': operator.contains
    }


@dataclass
class Expression:
    attr: Optional[str]
    op: Operator
    value: Any
    adapt_expected_value: bool = True
    case_sensitive: bool = False

    @classmethod
    def from_string(cls, string: str) -> Optional['Expression']:
        """
        Generate an expression from a string, which can later be used
        for comparison purposes with the attribute of an object:
        Examples:
        expr = Expression.from_string('method = login')

        class Test:
            def __init__(self, method: str):
                self.method = method

        t1 = test('login')
        t2 = test('logout)
        expr(t1)
        True
        expr(t2)
        False

        Case insensitive:
        expr = Expression.from_string('method i= login')

        Booleans:
        expr = Expression.from_string('params')
        expr = Expression.from_string('not params')

        Value is in expected value

        expr = Expression.from_string('method in logins')
        expr(t1)
        True
        expr(t2)
        False

        Value contains expected value
        expr = Expression.from_string('method contains log')
                expr(t1)
        True
        expr(t2)
        True
        """
        case_sensitive = False
        adapt_expected_value = True
        if string:
            if ' ' not in string:
                attr = string
                op = 'eq'
                adapt_expected_value = False
                value = True
            elif string.startswith('not '):
                attr = string.split('not ')[1]
                op = 'eq'
                adapt_expected_value = False
                value = False
            else:
                attr, op, value = string.split()
                if op.startswith('i') and not op == 'in':
                    case_sensitive = True
                    value = value.lower()
                    op = op.split('i', 1)[1]
            op = Operator(op)
            return cls(attr, op, value, adapt_expected_value=adapt_expected_value, case_sensitive=case_sensitive)
        return None

    def __call__(self, obj: Any) -> bool:
        if not self.attr or self.attr == 'self':
            value = obj
        else:
            value = getattr(obj, self.attr)
        if self.case_sensitive:
            if isinstance(value, (tuple, list)):
                value = [v.lower() for v in value]
            else:
                value = value.lower()
            return self.op(value, self.value)
        if self.adapt_expected_value:
            value_type = type(value)
            compare_value = value_type(self.value)
        else:
            value_type = type(self.value)
            value = value_type(value)
            compare_value = self.value
        return self.op(value, compare_value)
