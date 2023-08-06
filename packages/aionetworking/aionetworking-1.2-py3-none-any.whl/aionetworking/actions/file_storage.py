from abc import abstractmethod
import asyncio
from dataclasses import dataclass, field
import logging
from pathlib import Path

from .base import BaseAction
from aionetworking.logging.loggers import get_logger_receiver
from aionetworking import settings
from aionetworking.compatibility import create_task, set_task_name, Protocol
from aionetworking.logging.utils_logging import p
from aionetworking.futures.value_waiters import StatusWaiter
from aionetworking.utils import makedirs
from aionetworking.types.logging import LoggerType

from typing import Any, ClassVar, AnyStr
from aionetworking.types.formats import MessageObjectType


@dataclass
class ManagedFile:
    path: Path
    mode: str = 'ab'
    buffering: int = -1
    timeout: int = 10
    retries: int = 3
    retry_interval: int = 2
    logger: LoggerType = field(default_factory=get_logger_receiver)
    _status: StatusWaiter = field(default_factory=StatusWaiter, init=False)
    previous: 'ManagedFile' = field(default=None)
    _queue: asyncio.Queue = field(default_factory=asyncio.Queue, init=False, repr=False, hash=False, compare=False)
    _exception: OSError = field(default=None, init=False)
    _open_files: ClassVar = {}

    @classmethod
    def open(cls, path, *args, **kwargs) -> 'ManagedFile':
        try:
            f = cls._open_files[path]
            if not f.is_closing():
                return f
            kwargs['previous'] = f
        except KeyError:
            pass
        f = cls(path, *args, **kwargs)
        cls._open_files[path] = f
        return f

    @classmethod
    async def close_all(cls, base_path: Path = None) -> None:
        if base_path:
            files = [f for f in cls._open_files.values() if f.is_in(base_path)]
        else:
            files = [f for f in cls._open_files.values()]
        await asyncio.gather(*[f.close() for f in files])

    @classmethod
    def num_files(cls):
        return len(cls._open_files)

    def __post_init__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._task = create_task(self.manage())
        set_task_name(self._task, f"ManagedFile:{self.path.name}")

    def is_in(self, path) -> bool:
        try:
            self.path.relative_to(path)
            return True
        except ValueError:
            return False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    def is_closing(self):
        return self._status.has_started() and self._status.is_stopping_or_stopped()

    async def wait_closed(self):
        return await self._status.wait_stopped()

    async def wait_has_started(self):
        return await self._status.wait_has_started()

    def _cleanup(self) -> None:
        self._status.set_stopping()
        if self._open_files[self.path] == self:
            del self._open_files[self.path]
        self.logger.debug('Cleanup completed for %s', self.path)
        self._status.set_stopped()

    async def write(self, data: AnyStr) -> None:
        fut = asyncio.Future()
        if self._exception:
            fut.set_exception(self._exception)
        else:
            self._queue.put_nowait((data, fut))
            if self.logger.isEnabledFor(logging.DEBUG):
                qsize = self._queue.qsize()
                self.logger.debug('Message added to queue with future %s', id(fut))
                self.logger.debug('There %s now %s in the write queue %s for %s',
                                  p.plural_verb('is', qsize), p.no('item', qsize), id(self._queue), self.path)
        await fut

    async def close(self) -> None:
        if not self.is_closing():
            await self._status.wait_started()
            self._status.set_stopping()
            self.logger.debug('Closing file %s', self.path)
            if not self._task.done():
                await self.wait_has_started()
                await self.wait_writes_done()
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass
            else:
                self.logger.debug('File %s already closed', self.path)
            self.logger.debug('Closed file %s', self.path)

    async def wait_writes_done(self) -> None:
        self.logger.debug('Waiting for writes to complete for %s', self.path)
        done, pending = await asyncio.wait([self._queue.join(), self._task], return_when=asyncio.FIRST_COMPLETED)
        for d in done:
            if d.exception():                       #3.8 assignment expressions
                self.logger.error(d.exception())
                await d
        self.logger.debug('Writes completed for %s', self.path)

    def _task_done(self, num: int) -> None:
        for _ in range(0, num):
            self._queue.task_done()
        self.logger.info('Task done set for %s on file %s', p.no('item', num), self.path)

    async def manage_wrapper(self):
        if self.previous:
            await self.previous.wait_closed()
        for i in range(0, self.retries):
            try:
                await self.manage()
                return
            except OSError as e:
                if i == 3:
                    self._exception = e
                    while not self._queue.empty():
                        try:
                            item, fut = self._queue.get_nowait()
                            fut.set_exception(e)
                            self._task_done(1)
                        except asyncio.QueueEmpty:
                            self.logger.info('QueueEmpty error was unexpectedly caught for file %s', self.path)
                await asyncio.sleep(self.retry_interval)

    async def _write_items_from_queue(self, f):
        self.logger.info('Retrieving item from queue for file %s. Timeout: %s', self.path,
                         p.no('second', self.timeout))
        try:
            data, fut = self._queue.get_nowait()
        except asyncio.QueueEmpty:
            data, fut = await asyncio.wait_for(self._queue.get(), timeout=self.timeout)
        futs = [fut]
        try:
            while not self._queue.empty():
                try:
                    item, fut = self._queue.get_nowait()
                    data += item
                    futs.append(fut)
                except asyncio.QueueEmpty:
                    self.logger.warning('QueueEmpty error was unexpectedly caught for file %s', self.path)
            self.logger.info('Retrieved %s from queue. Writing to file %s.', p.no('item',
                                                                                  len(futs)), self.path)
            await f.write(data)
            self.logger.info('%s written to file %s', p.no('byte', len(data)), self.path)
            for fut in futs:
                fut.set_result(True)
                self.logger.debug('Result set on future %s', id(fut))
        except Exception as e:
            for fut in futs:
                fut.set_exception(e)
        finally:
            asyncio.get_event_loop().call_soon(self._task_done, len(futs))

    async def manage(self) -> None:
        self._status.set_starting()
        await makedirs(self.path.parent, exist_ok=True)
        self.logger.info('Opening file %s', self.path)
        async with settings.FILE_OPENER(self.path, mode=self.mode, buffering=self.buffering) as f:
            try:
                self.logger.debug('File %s opened', self.path)
                self._status.set_started()
                while True:
                    try:
                        await self._write_items_from_queue(f)
                    except asyncio.TimeoutError:
                        qsize = self._queue.qsize()
                        if qsize:
                            self.logger.warning(
                                'Get item for file %s timed out out even though there %s %s in the queue id %s',
                                self.path, p.plural_verb('is', qsize), p.no('item', qsize), id(self._queue))
                            await self._write_items_from_queue(f)
                        else:
                            self.logger.info('File %s closing due to timeout on new items to write', self.path)
                            break
            except asyncio.CancelledError as e:
                self.logger.info('File %s closing due to task being cancelled', self.path)
                raise e
            finally:
                self._cleanup()
                qsize = self._queue.qsize()
                if qsize:
                    self.logger.warning(
                        'There %s %s in queue id %s for path %s even after cleanup',
                        p.plural_verb('is', qsize), p.no('item', qsize), id(self._queue), self.path)
                    await self._write_items_from_queue(f)
        self.logger.info('File %s closed', self.path)


def default_data_dir():
    return settings.DATA_DIR


@dataclass
class BaseFileStorage(BaseAction, Protocol):
    base_path: Path = field(default_factory=default_data_dir, metadata={'pickle': True})
    path: str = ''
    attr: str = 'encoded'
    mode: str = 'wb'
    separator: AnyStr = ''

    def __post_init__(self):
        if 'b' in self.mode:
            if isinstance(self.separator, str):
                self.separator = self.separator.encode()
        self._status.is_started()
        settings.ACTION_CONFIG = {
            'base_path': self.base_path,
            'path': self.path,
            'attr': self.attr,
            'mode': self.mode,
            'separator': self.separator
        }

    def _get_full_path(self, msg: MessageObjectType) -> Path:
        return self.base_path / self._get_path(msg)

    def _get_path(self, msg: MessageObjectType) -> Path:
        return Path(self.path.format(msg=msg))

    def _get_data(self, msg: MessageObjectType) -> AnyStr:
        data = getattr(msg, self.attr)
        if self.separator:
            data += self.separator
        return data

    @abstractmethod
    async def _write_to_file(self, path: Path, data: AnyStr): ...

    async def write_one(self, msg: MessageObjectType) -> Path:
        path = self._get_full_path(msg)
        msg.logger.debug('Writing to file %s', path)
        data = self._get_data(msg)
        await self._write_to_file(path, data)
        msg.logger.debug('Data written to file %s', path)
        return path

    async def do_one(self, msg: MessageObjectType) -> Any:
        self._status.set_started()
        if getattr(msg, 'store', True):
            await self.write_one(msg)
        return getattr(msg, 'response', None)


@dataclass
class FileStorage(BaseFileStorage):
    name = 'File Storage'

    async def _write_to_file(self, path: Path, data: AnyStr) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        async with settings.FILE_OPENER(path, self.mode) as f:
            await f.write(data)


@dataclass
class BufferedFileStorage(BaseFileStorage):
    name = 'Buffered File Storage'
    mode: str = 'ab'
    _qsize: int = 0

    close_file_after_inactivity: int = 10
    buffering: int = -1

    async def _write_to_file(self, path: Path, data: AnyStr) -> None:
        async with ManagedFile.open(path, mode=self.mode, buffering=self.buffering,
                                    timeout=self.close_file_after_inactivity, logger=self.logger) as f:
            await f.write(data)

    async def close(self) -> None:
        self._status.set_stopping()
        await ManagedFile.close_all(base_path=self.base_path)
        self._status.set_stopped()
