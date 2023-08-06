"""
Protocol messages sent between PCSC-lite client and server. PCSC-lite assumes that server and
client run on the same machine, the serialization is done through C structs. There may be
variations in byte order. In theory, padding could vary too because of alignment requirements.
We assume a 32 bit alignment which appears to work with 32 and 64 bit linux systems.

Byte order can be controlled, e.g. when client and server run on different architectures.
Defaults to using the system's native byte order.
"""

from __future__ import annotations

import struct
from contextlib import asynccontextmanager
from dataclasses import InitVar, astuple, dataclass, field, fields, Field
from typing import ByteString, List, Any, Type, Dict

from . import const
from .exception import ScardException


def _param(typ: Any, fmt: str, doc: str) -> Field:
    """
    Used to specify a parameter for a dataclass.

    Args:
        typ: python type to annotate parameter with
        fmt: Format string for struct.pack/.unpack
        doc: DocString for this parameter

    Returns:
        Field for the dataclass parameter.
    """

    return field(metadata={"typ": typ, "fmt": fmt, "doc": doc})


def _int32(doc: str) -> Field:
    """
    Signed 32 bit integer parameter.

    Args:
        doc: DocString for this parameter

    Returns:
        Field for the dataclass parameter.
    """

    return _param(int, "i", doc)


def _uint32(doc: str) -> Field:
    """
    Unsigned 32 bit integer parameter.

    Args:
        doc: DocString for this parameter

    Returns:
        Field for the dataclass parameter.
    """

    return _param(int, "I", doc)


def _char_array(size: int, doc: str) -> Field:
    """
    Character string, zero padded to next multiple of 4 bytes.

    Args:
        doc: DocString for this parameter

    Returns:
        Field for the dataclass parameter.
    """

    return _param(bytes, f"{size}s{-size % 4}x", doc)


class ProtocolMeta(type):
    """
    Meta Class which creates a proper data class and sets some class variables
    """

    def __new__(cls, name, bases, dct, cmd=None):
        # Ignore ProtocolMessage base class alone
        if cmd is None:
            return super().__new__(cls, name, bases, dct)

        self = super().__new__(cls, name, bases, dct, cmd=cmd)

        # Empty message types inherit annotations from the base class. Detect this and empty the annotations.
        if "_subs" in self.__annotations__:
            self.__annotations__ = {}

        # Create dataclass attributes and annotations
        for k, v in self.__annotations__.items():
            # annotations are strings.
            v = eval(v)

            self.__annotations__[k] = v.metadata["typ"]
            setattr(self, k, v)

        # Expect that every class is initiated with a "byteorder" parameter
        self.__annotations__["byteorder"] = InitVar[str]

        # Apply dataclass decorator
        self = dataclass(self)

        # Create struct format string
        fmt = "".join(f.metadata["fmt"] for f in fields(self))

        # Calculate message size
        self._size = struct.calcsize(f"={fmt}")

        # Create class attribues
        self._fmt = fmt
        self._cmd = cmd

        return self


class ProtocolMessage(metaclass=ProtocolMeta):
    """
    Base class for all protocol messages.
    """

    # Used by server implementations to convert messages to the correct type.
    _subs: Dict[int, Type[ProtocolMessage]] = {}

    # Byte order, one of "<", "=", ">" for little, native or big endian.
    _byteorder: str

    # Message size class attribute, set by meta class.
    _size: int

    # Message format class attribute excluding byte order, set by meta class.
    _fmt: str

    # Message command class attribute, set by meta class.
    _cmd: int

    def __init_subclass__(cls, cmd: int, **kwargs: Dict[str, Any]) -> None:
        """
        Register sub class
        """

        if cmd >= 0:
            cls._subs[cmd] = cls
        super().__init_subclass__(**kwargs)

    def __post_init__(self, byteorder: str) -> None:
        """
        Process `byteorder` InitVar that was added by meta class.

        Args:
            byteorder: Byte order, one of "<", "=", ">" for little, native or big endian.
        """

        self._byteorder = byteorder

    @property
    def encoded_req(self) -> bytes:
        """
        Encode this message as a PCSC-lite request.

        Returns:
            Encoded message
        """

        return struct.pack(
            f"{self._byteorder}II{self._fmt}", self._size, self._cmd, *astuple(self)
        )

    @property
    def encoded_resp(self) -> bytes:
        """
        Encode this message as a PCSC-lite response.

        Returns:
            Encoded message
        """

        return struct.pack(f"{self._byteorder}{self._fmt}", *astuple(self))

    @classmethod
    def decode(cls, buf: ByteString, byteorder: str) -> ProtocolMessage:
        """
        Decode a message (excluding length / command)

        Args:
            buf: message to decode
            byteorder: one of "<", "=", ">" for little, native or big endian.

        Returns:
            Decoded message.
        """

        # Convert all fields to their correct type
        values = (
            fld.type(value)
            for value, fld in zip(struct.unpack(byteorder + cls._fmt, buf), fields(cls))
        )
        return cls(*values, byteorder=byteorder)


class CmdVersion(ProtocolMessage, cmd=const.MsgCommand.VERSION):
    """
    Negotiate protocol version. Needs to be sent as first message.
    """

    major: _int32("Major protocol version")
    minor: _int32("Minor protocol version")
    rv: _uint32("Return value")


class ScardEstablishContext(ProtocolMessage, cmd=const.MsgCommand.ESTABLISH_CONTEXT):
    """
    Creates an Application Context to the PC/SC Resource Manager.
    """

    scope: _param(const.ScardScope, "I", "Scope")
    context: _uint32("Context")
    rv: _uint32("Return value")


class SCardReleaseContext(ProtocolMessage, cmd=const.MsgCommand.RELEASE_CONTEXT):
    """
    Destroys a communication context to the PC/SC Resource Manager.
    """

    context: _uint32("Context")
    rv: _uint32("Return value")


class SCardCancel(ProtocolMessage, cmd=const.MsgCommand.CANCEL):
    """
    Really just the same as CmdStopWaitingReaderStateChange. Don't use.
    """

    context: _uint32("Context")
    rv: _uint32("Return value")


class SCardConnect(ProtocolMessage, cmd=const.MsgCommand.CONNECT):
    """
    Establishes a connection to the reader specified in `reader`.
    """

    context: _uint32("Context")
    reader: _char_array(const.MAX_READERNAME, "Reader name")
    share_mode: _param(const.ScardShare, "I", "Share mode")
    preferred_protocols: _param(const.ScardProtocol, "I", "Preferred Protocols")
    card: _int32("Card")
    active_protocol: _param(const.ScardProtocol, "I", "Active Protocol")
    rv: _uint32("Return value")


class SCardReconnect(ProtocolMessage, cmd=const.MsgCommand.RECONNECT):
    """
    Reestablishes a connection to a reader that was previously connected to using
    SCardConnect().
    """

    card: _int32("Card")
    share_mode: _param(const.ScardShare, "I", "Share mode")
    preferred_protocols: _param(const.ScardProtocol, "I", "Preferred Protocols")
    initialization: _uint32("Initialization")
    active_protocol: _param(const.ScardProtocol, "I", "Active Protocol")
    rv: _uint32("Return value")


class SCardDisconnect(ProtocolMessage, cmd=const.MsgCommand.DISCONNECT):
    """
    Terminates a connection made through SCardConnect().
    """

    card: _int32("Card")
    disposition: _param(const.Disposition, "I", "Disposition")
    rv: _uint32("Return value")


class SCardBeginTransaction(ProtocolMessage, cmd=const.MsgCommand.BEGIN_TRANSACTION):
    """
    Establishes a temporary exclusive access mode for doing a series of commands in a
    transaction.
    """

    card: _int32("Card")
    rv: _uint32("Return value")


class SCardEndTransaction(ProtocolMessage, cmd=const.MsgCommand.END_TRANSACTION):
    """
    Ends a previously begun transaction.
    """

    card: _int32("Card")
    disposition: _param(const.Disposition, "I", "Disposition")
    rv: _uint32("Return value")


class SCardTransmit(ProtocolMessage, cmd=const.MsgCommand.TRANSMIT):
    """
    Sends an APDU to the smart card contained in the reader connected to by SCardConnect().
    """

    card: _int32("Card")
    send_pci_protocol: _uint32("ioSendPciProtocol")
    send_pci_length: _uint32("ioSendPciLength")
    send_length: _uint32("cbSendLength")
    recv_pci_protocol: _uint32("ioRecvPciProtocol")
    recv_pci_length: _uint32("ioRecvPciLength")
    recv_length: _uint32("pcbRecvLength")
    rv: _uint32("Return value")


class SCardControl(ProtocolMessage, cmd=const.MsgCommand.CONTROL):
    """
    Sends a command directly to the IFD Handler (reader driver) to be processed by the reader.
    """

    card: _int32("Card")
    control_code: _uint32("Control Code")
    send_length: _uint32("cbSendLength")
    recv_length: _uint32("pcbRecvLength")
    bytes_returned: _uint32("Bytes Returned")
    rv: _uint32("Return value")


class SCardStatus(ProtocolMessage, cmd=const.MsgCommand.STATUS):
    """
    Returns the current status of the reader connected to by `card`.
    """

    card: _int32("Card")
    rv: _uint32("Return value")


class SCardGetAttrib(ProtocolMessage, cmd=const.MsgCommand.GET_ATTRIB):
    """
    Get an attribute from the IFD Handler (reader driver).
    """

    card: _int32("Card")
    attr_id: _uint32("Attribute ID")
    attr: _char_array(264, "Attribute")
    attr_len: _uint32("Attribute Length")
    rv: _uint32("Return value")


class SCardSetAttrib(ProtocolMessage, cmd=const.MsgCommand.SET_ATTRIB):
    """
    Set an attribute of the IFD Handler.
    """

    card: _int32("Card")
    attr_id: _uint32("Attribute ID")
    attr: _char_array(264, "Attribute")
    attr_len: _uint32("Attribute Length")
    rv: _uint32("Return value")


class CmdGetReadersState(ProtocolMessage, cmd=const.MsgCommand.GET_READERS_STATE):
    """
    Get current state of readers. Will be responded to with MAX_READERS_CONTEXTS times
    MsgReaderState.
    """


class CmdWaitReaderStateChange(ProtocolMessage, cmd=const.MsgCommand.WAIT_READER_STATE_CHANGE):
    """
    Get current state of readers and wait for a change in the state.
    Will be responded to with MAX_READERS_CONTEXTS times MsgReaderState.
    On change or when the client sends CmdStopWaitingReaderStateChange,
    WaitReaderStateChange is sent.
    """


class CmdStopWaitingReaderStateChange(
    ProtocolMessage, cmd=const.MsgCommand.STOP_WAITING_READER_STATE_CHANGE
):
    """
    Cancel a running CmdWaitReaderStateChange.
    """


class WaitReaderStateChange(ProtocolMessage, cmd=-1):
    """
    Response to CmdWaitReaderStateChange.
    """

    timeout: _uint32("Timeout")
    rv: _uint32("Return value")


class MsgReaderState(ProtocolMessage, cmd=-1):
    """
    Returned MAX_READERS_CONTEXTS times after sending CmdGetReadersState or
    CmdWaitReaderStateChange
    """

    # reader_name is zero padded (at least 1 byte)
    reader_name: _char_array(const.MAX_READERNAME, "Reader Name")
    event_counter: _uint32("Event Counter")
    reader_state: _param(const.ReaderState, "I", "Reader State")
    reader_sharing: _int32("Reader Sharing")  # ScardSharing or integer
    card_atr: _char_array(33, "Answer To Reset")
    card_atr_length: _uint32("Length of ATR")
    card_protocol: _param(const.ScardProtocol, "I", "Protocol")
