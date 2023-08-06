import asyncio
from abc import abstractmethod
import datetime
from dataclasses import dataclass, field
from pathlib import Path

from aionetworking.types.actions import ActionType
from aionetworking.types.requesters import RequesterType
from aionetworking.types.logging import LoggerType
from aionetworking.types.formats import MessageObjectType
from aionetworking.utils import inherit_on_type_checking_only

from aionetworking.types.networking import AdaptorType
from .transports import TransportType

from aionetworking.compatibility import Protocol
from typing import Any, AsyncGenerator, Generator, Optional, Sequence, Union, Dict, Tuple, Type


class ProtocolFactoryProtocol(Protocol):

    @abstractmethod
    def __call__(self) -> Union['ProtocolFactoryProtocol', 'NetworkConnectionProtocol']: ...

    @abstractmethod
    def is_owner(self, connection: 'NetworkConnectionProtocol') -> bool: ...

    @abstractmethod
    def set_name(self, name: str, peer_prefix: str): ...

    @abstractmethod
    async def wait_all_closed(self) -> None: ...

    @abstractmethod
    async def wait_num_has_connected(self, num: int) -> None: ...

    @abstractmethod
    async def close_actions(self) -> None: ...

    @abstractmethod
    async def start(self, logger: LoggerType = None) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...


@dataclass
class ConnectionProtocol(Protocol):

    @property
    @abstractmethod
    def peer(self) -> str: ...

    @abstractmethod
    def is_child(self, parent_name: str) -> bool: ...

    @abstractmethod
    def finish_connection(self, exc: Optional[BaseException]) -> None: ...

    @abstractmethod
    async def wait_closed(self) -> None: ...

    @abstractmethod
    async def wait_connected(self) -> None: ...

    @abstractmethod
    def is_connected(self) -> bool: ...

    @abstractmethod
    def send(self, data: bytes) -> Optional[asyncio.Future]: ...


@dataclass
class ConnectionDataclassProtocol(ConnectionProtocol, Protocol):
    name = None

    parent_name: str = None
    action: ActionType = None
    preaction: ActionType = None
    requester: RequesterType = None
    dataformat: Type[MessageObjectType] = None
    context: Dict[str, Any] = field(default_factory=dict, metadata={'pickle': True})
    peer_prefix: str = ''
    last_msg: datetime.datetime = field(default=None, init=False, compare=False, hash=False)
    timeout: Union[int, float] = None

    adaptor_cls: Type[AdaptorType] = field(default=None, init=False)
    _adaptor: AdaptorType = field(default=None, init=False)


@dataclass
class NetworkConnectionProtocol(ConnectionDataclassProtocol, Protocol):
    @abstractmethod
    def initialize_connection(self, transport: TransportType, peer: Tuple[str, int] = None) -> bool: ...


@dataclass
class SimpleNetworkConnectionProtocol(Protocol):
    peer: str
    parent_name: str
    queue: asyncio.Queue

    @abstractmethod
    def encode_and_send_msg(self, msg_decoded: Any) -> None: ...


class UDPConnectionMixinProtocol(Protocol): ...


class UDPConnectionProtocol(UDPConnectionMixinProtocol, NetworkConnectionProtocol, Protocol):  ...


class BaseAdaptorProtocol(Protocol):

    @abstractmethod
    def send_data(self, msg_encoded: bytes) -> asyncio.Future: ...

    @abstractmethod
    def encode_and_send_msg(self, msg_decoded: Any) -> None: ...

    @abstractmethod
    def encode_and_send_msgs(self, decoded_msgs: Sequence[Any]) -> None: ...

    @abstractmethod
    def on_data_received(self, buffer: bytes, timestamp: datetime.datetime = None) -> asyncio.Future: ...


class AdaptorProtocol(BaseAdaptorProtocol, Protocol):

    @abstractmethod
    async def close(self, exc: Optional[BaseException] = None) -> None: ...


@inherit_on_type_checking_only
class AdaptorProtocolGetattr(BaseAdaptorProtocol, Protocol):

    def send_data(self, msg_encoded: bytes) -> None: ...

    def encode_and_send_msg(self, msg_decoded: Any) -> None: ...

    def encode_and_send_msgs(self, decoded_msgs: Sequence[Any]) -> None: ...

    def on_data_received(self, buffer: bytes, timestamp: datetime.datetime = None) -> asyncio.Future: ...


class SenderAdaptorMixinProtocol(Protocol):
    @abstractmethod
    async def wait_notification(self) -> MessageObjectType: ...

    @abstractmethod
    def get_notification(self) -> MessageObjectType: ...

    @abstractmethod
    async def wait_notifications(self) -> AsyncGenerator[MessageObjectType, None]:
        yield

    @abstractmethod
    def all_notifications(self) -> Generator[MessageObjectType, None, None]: ...

    @abstractmethod
    async def send_data_and_wait(self, request_id: Any, encoded: bytes) -> asyncio.Future: ...

    @abstractmethod
    async def send_msg_and_wait(self, msg_obj: MessageObjectType) -> asyncio.Future: ...

    @abstractmethod
    async def encode_send_wait(self, decoded: Any) -> asyncio.Future: ...

    @abstractmethod
    async def play_recording(self, file_path: Path, hosts: Sequence = (), timing: bool = True) -> None: ...


class SenderAdaptorProtocol(ConnectionProtocol, Protocol): ...


@inherit_on_type_checking_only
class SenderAdaptorGetattr(SenderAdaptorMixinProtocol, Protocol):
    async def wait_notification(self) -> MessageObjectType: ...

    def get_notification(self) -> MessageObjectType: ...

    async def wait_notifications(self) -> AsyncGenerator[MessageObjectType, None]:
        yield

    def all_notifications(self) -> Generator[MessageObjectType, None, None]: ...

    async def send_data_and_wait(self, request_id: Any, encoded: bytes) -> asyncio.Future: ...

    async def send_msg_and_wait(self, msg_obj: MessageObjectType) -> asyncio.Future: ...

    async def encode_send_wait(self, decoded: Any) -> asyncio.Future: ...

    async def play_recording(self, file_path: Path, hosts: Sequence = (), timing: bool = True) -> None: ...
