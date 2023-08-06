from __future__ import annotations

import anyio.abc
import anyio.streams.buffered
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from . import const, proto
from .exception import ScardException
import re
from dataclasses import dataclass

SOCKET_PATHS = ["/run/pcscd/pcscd.comm"]


class PcscClient:
    reader_state: List[PcscReader]
    _sock: anyio.abc.ByteStream
    _recv_sock: anyio.streams.buffered.BufferedByteReceiveStream
    _byteorder: str

    def __init__(self, sock: anyio.abc.ByteStream, byteorder: str = "=") -> None:
        """
        Args:
            sock: socket connected to PC/SC Daemon
            byteorder: '<', '=', '>' for little, native and big endian.
        """

        self._sock = sock
        self._recv_sock = anyio.streams.buffered.BufferedByteReceiveStream(sock)
        self._byteorder = byteorder

    @classmethod
    @asynccontextmanager
    async def connect(
        cls, path: Optional[str] = None, byteorder: str = "="
    ) -> AsyncGenerator[PcscClient, None]:
        """
        Connect to the PC/SC Daemon

        Args:
            path: unix socket path. If None, try some well-known paths.
            byteorder: '<', '=', '>' for little, native and big endian.

        Returns:
            A PcscClient instance
        """

        for pcsc_path in [path] if path else SOCKET_PATHS:
            try:
                sock = await anyio.connect_unix(pcsc_path)
            except OSError as ex:
                last_ex = ex
            else:
                async with sock:
                    yield cls(sock, byteorder)
                    break

    async def _recv_msg(self, cls):
        resp = await self._recv_sock.receive_exactly(cls._size)
        msg = cls.decode(resp, byteorder=self._byteorder)
        try:
            rv = msg.rv
        except AttributeError:
            return msg
        if rv:
            raise ScardException.create(msg, rv)
        return msg

    async def _recv_msg_n(self, cls, count):
        for __ in range(count):
            yield await self._recv_msg(cls)

    async def _send_msg(self, cls, *args, **kwargs):
        data = cls(*args, **kwargs, byteorder=self._byteorder).encoded_req
        await self._sock.send(data)

    async def query(self, cls, *args, **kwargs):
        await self._send_msg(cls, *args, **kwargs)
        return await self._recv_msg(cls)

    async def cmd_version(self, major=4, minor=4):
        return await self.query(proto.CmdVersion, major, minor, 0)

    async def get_reader_state(self):
        await self._send_msg(proto.CmdGetReadersState)
        return await self._read_reader_state()

    async def wait_reader_state_change(self):
        """
        After sending CmdWaitReaderStateChange, the server will directly send the current
        list of reader states. After a change or after receiving CmdStopWaitingReaderStateChange,
        the reply to CmdWaitReaderStateChange will be sent to the client.
        """

        try:
            cur_state = self.reader_state
        except AttributeError as ex:
            raise RuntimeError(
                "get_reader_state() must have been called at least once before"
            ) from ex

        while True:
            await self._send_msg(proto.CmdWaitReaderStateChange)
            new_state = await self._read_reader_state()
            if new_state != cur_state:
                await self._send_msg(proto.CmdStopWaitingReaderStateChange)
                await self._recv_msg(proto.WaitReaderStateChange)
                return new_state

            # XXX make cancellable
            await self._recv_msg(proto.WaitReaderStateChange)
            # XXX make cancellable

            new_state = await self.get_reader_state()
            if new_state != cur_state:
                return new_state
            cur_state = new_state

    async def _read_reader_state(self):
        self.reader_state = [
            PcscReader(self, rs)
            async for rs in self._recv_msg_n(proto.MsgReaderState, const.MAX_READERS_CONTEXTS)
            if rs.reader_state
        ]
        return self.reader_state


class PcscReader:
    """
    Represents a chipcard reader (IFD)
    """

    _re_name = re.compile(r"^(.*) ([0-9A-F]{2}) 00$")

    _rs: proto.MsgReaderState
    client: PcscClient

    def __init__(self, client: PcscClient, rs: MsgReaderState) -> None:
        self.client = client
        self._rs = rs

    @property
    def full_name(self) -> str:
        result = self._rs.reader_name.rstrip(b"\x00").decode("latin1")
        if "\0" in result:
            raise ValueError(result)

        return result

    @property
    def name(self) -> str:
        m = self._re_name.match(self.full_name)
        if not m:
            raise ValueError(self.full_name)

        return m.group(1)

    @property
    def reader_id(self) -> int:
        m = self._re_name.match(self.full_name)
        if not m:
            raise ValueError(self.full_name)

        return int(m.group(2), 16)

    @property
    def atr(self) -> bytes:
        return self._rs.card_atr[: self._rs.card_atr_length]

    @property
    def event_counter(self) -> int:
        return self._rs.event_counter

    @property
    def reader_state(self) -> const.ReaderState:
        return self._rs.reader_state

    @property
    def reader_sharing(self) -> const.ScardShare:
        return self._rs.reader_sharing

    @property
    def card_protocol(self) -> const.ScardProtocol:
        return self._rs.card_protocol

    @asynccontextmanager
    async def connect(
        self,
        scope: const.ScardScope = const.ScardScope.SYSTEM,
        share_mode: const.ScardShare = const.ScardShare.SHARED,# XXX EXCLUSIVE,
        preferred_protocols: const.ScardProtocol = const.ScardProtocol.ANY,
        disposition: const.Disposition = const.Disposition.RESET,
    ) -> AsyncGenerator[PcscCard, None]:
        """
        Args:
            scope: Is ignored by pcscd.
            share_mode: Controls if/how other applications may use the reader at the same time.
            preferred_protocols: Protocol (T0, T1, etc.) to use.
            disposition: Action on disconnect.
        """
        ctx = await self.client.query(proto.ScardEstablishContext, scope, 0, 0)
        try:
            conn = await self.client.query(
                proto.SCardConnect,
                ctx.context,
                self._rs.reader_name,
                share_mode,
                preferred_protocols,
                0,
                0,
                0,
            )
            try:
                yield PcscCard(self, conn.card, conn.active_protocol)
            finally:
                await self.client.query(proto.SCardDisconnect, conn.card, disposition, 0)
        finally:
            await self.client.query(proto.SCardReleaseContext, ctx.context, 0)

    def __str__(self) -> str:
        return (
            f"PcscReader(reader_id={self.reader_id}, name={self.name!r}, atr={self.atr.hex()!r}, "
            f"event_counter={self.event_counter}, reader_state={self.reader_state!r}, "
            f"reader_sharing={self.reader_sharing!r}, card_protocol={self.card_protocol!r})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcscReader):
            return False

        return self._rs == other._rs


class PcscCard:
    """
    Represents a chipcard (ICC).
    """

    client: PcscClient
    reader: PcscReader
    card: int
    active_protocol: const.ScardProtocol

    def __init__(self, reader: PcscReader, card: int, active_protocol: const.ScardProtocol) -> None:
        """
        """

        self.client = reader.client
        self.reader = reader
        self.card = card
        self.active_protocol = active_protocol

    async def transmit(
        self, data: ByteString, protocol: const.ScardProtocol = None
    ) -> bytes:
        """
        Args:
            data: Data to transmit
            protocol: Protocol to use, defaults to current protocol.
        """

        await self.client._send_msg(
            proto.SCardTransmit,
            self.card,
            protocol or self.active_protocol,
            const.SIZEOF_SCARD_IO_REQUEST,
            len(data),
            0,
            0,
            const.MAX_BUFFER_SIZE_EXTENDED,
            0,
        )
        await self.client._sock.send(data)
        msg = await self.client._recv_msg(proto.SCardTransmit)
        resp = await self.client._recv_sock.receive_exactly(msg.recv_length)
        return resp

    @asynccontextmanager
    async def transaction(self, disposition: const.Disposition=const.Disposition.LEAVE):
        await self.client.query(
            proto.SCardBeginTransaction,
            self.card,
            0,
        )
        yield self
        await self.client.query(proto.SCardEndTransaction, self.card, disposition, 0)
