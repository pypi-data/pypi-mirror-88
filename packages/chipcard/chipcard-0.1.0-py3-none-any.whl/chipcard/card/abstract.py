"""
"""

from __future__ import annotations

from typing import ByteString, Any, Tuple, Union, Mapping, Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from asn1crypto.core import ObjectIdentifier


class FileControlInformation:
    def __init__(self, data: bytes) -> None:
        self.data = data

    def __bytes__(self) -> bytes:
        return self.data


class AbstractChipCard(ABC):
    def __init__(self, card) -> None:
        self.card = card
    
    async def send(self, cla: int, ins: int, p1: int, p2: int, data: ByteString, expected_length: int) -> ApduResponse:
        # XXX determine allow_extended from hysterical bytes or ATR
        apdu = encode_apdu_command(cla, ins, p1, p2, data, expected_length, True)
        resp = await self.card.transmit(apdu)
        
        response = ApduResponse(resp[:-2], resp[-2], resp[-1])
        response.raise_for_error()
        return response

    async def ins_select(self, cla: int, p1: int, p2: int, name: ByteString, expected: int) -> Optional[FileControlInformation]:
        resp = await self.send(cla, 0xa4, p1, p2, name, expected)
        return FileControlInformation(resp.data) if resp else None

    async def ins_verify_password(self, cla: int, p1: int, p2: int, data: ByteString) -> None:
        await self.send(cla, 0x20, p1, p2, data, 0)

    async def ins_terminate_df(self, cla) -> None:
        await self.send(cla, 0xe6, 0, 0, b'', 0)

    async def ins_get_challenge(self, count: int):
        return await self.send(0, 0x84, 0, 0, b'', count)

    async def ins_activate_current_file(self, cla) -> None:
        await self.send(cla, 0x44, 0, 0, b"", 0)

    async def ins_get_data(self, cla: int, p1: int, p2: int) -> bytes:
        resp = await self.send(cla, 0xca, p1, p2, b'', 65536)
        return resp.data

    async def ins_get_next_data(self, cla: int, p1: int, p2: int) -> bytes:
        resp = await self.send(cla, 0xcc, p1, p2, b'', 65536)
        return resp.data

    async def ins_put_data(self, cla: int, p1: int, p2: int, data: ByteString) -> None:
        await self.send(cla, 0xda, p1, p2, data, 0)

    @abstractmethod
    async def is_usable(self) -> bool:
        """
        """


class ApduException(Exception):
    def __init__(self, response: ApduResponse) -> None:
        self.response = response


@dataclass
class ApduResponse:
    data: bytes
    sw1: int
    sw2: int

    @property
    def sw(self):
        return self.sw1, self.sw2

    def __len__(self):
        return len(self.data)

    def __bytes__(self):
        return self.data

    def raise_for_error(self):
        if self.sw != (0x90, 0x00):
            raise ApduException(self)


def encode_apdu_command(
    cla: int,
    ins: int,
    p1: int,
    p2: int,
    data: ByteString,
    expected_length: int,
    allow_extended: bool,
) -> bytearray:
    """
    Encode an APDU command.

    If allow_extended is not set, data must be at most 255 bytes and expected_length at most 256.
    Otherwise, data can be up to 65535 bytes and expected_length can be 65536.

    Args:
        cla: class byte
        ins: instruction byte
        p1: first parameter byte
        p2: second parameter byte
        data: command data to transmit
        expected_length: expected length
        allow_extended: extended length allowed

    Returns:
        Encoded APDU

    Raises:
        ValueError: data or expected_length too long.
    """

    max_len = 65536 if allow_extended else 256

    if len(data) >= max_len:
        raise ValueError(f"Data too long: {len(data)}")

    if expected_length > max_len:
        raise ValueError(f"Expected length too long: {expected_length}")

    buf = bytearray((cla, ins, p1, p2))

    if len(data) < 256 and expected_length <= 256:
        # short fields
        if data:
            buf.append(len(data))
            buf.extend(data)
        if expected_length:
            buf.append(expected_length & 0xFF)
    else:
        # long fields
        if data:
            buf.extend((0, len(data) >> 8, len(data) & 0xFF))
            buf.extend(data)
        if expected_length:
            if not data:
                buf.append(0)
            if expected_length == 65536:
                buf.extend((0, 0))
            else:
                buf.extend((expected_length >> 8, expected_length & 0xFF))
    return buf


def decode_apdu_command(buf: ByteString) -> Tuple[int, int, int, int, bytes, int, bool]:
    """
    Reverse of encode_apdu_command to parse an encoded command.

    Args:
        buf: An encoded APDU command

    Returns:
        cla, ins, p1, p2, data, expected_length, extended

    Raises:
        ValueError: bad encoding.
    """

    cla, ins, p1, p2 = buf[:4]
    rem = len(buf) - 4

    # Parse short fields

    if rem == 0:
        return cla, ins, p1, p2, b"", 0, False

    if rem == 1:
        return cla, ins, p1, p2, b"", buf[4] or 256, False

    if buf[4] != 0:
        if rem - 1 == buf[4]:
            return cla, ins, p1, p2, bytes(buf[5:]), 0, False

        if rem - 1 == buf[4] + 1:
            return cla, ins, p1, p2, bytes(buf[5:-1]), buf[-1] or 256, False

        raise ValueError

    if rem == 2:
        raise ValueError

    # Parse extended fields

    tmp = (buf[5] << 8) | buf[6]
    if rem == 3:
        return cla, ins, p1, p2, b"", tmp or 65536, True

    if rem - 3 == tmp:
        return cla, ins, p1, p2, bytes(buf[7:]), 0, True

    if rem - 3 == tmp + 2:
        return cla, ins, p1, p2, bytes(buf[7:-2]), ((buf[-2] << 8) | buf[-1]) or 65536, True

    raise ValueError


def decode_compact_tlv(data: ByteString) -> Dict[int, bytes]:
    """
    Args:
        data: COMPACT-TLV encoded data

    Returns:
        Dictionary where key is the tag and value the value.

    Raises:
        ValueError: Badly encoded TLV
    """

    pos = 0
    result = {}

    while pos < len(data):
        tag, length = divmod(data[pos], 16)
        pos += 1
        if length > len(data) - pos:
            raise ValueError(
                f"Tried to read {length} bytes for tag {tag}, but only {len(data) - pos} are"
                " available."
            )
        result[tag] = bytes(data[pos : pos + length])
        pos += length

    return result


def encode_compact_tlv(data: Mapping[int, ByteString]) -> bytes:
    """
    Args:
        data: Mapping from tags to values

    Returns:
        COMPACT-TLV encoded data

    Raises:
        ValueError: Tag or Length too big
    """

    result = b""
    for tag, value in data.items():
        if not 0 <= tag <= 15:
            raise ValueError(f"Tag {tag} out of range [0, 15]")
        if len(value) > 15:
            raise ValueError(f"Value of tag {tag} too big: {len(value)}")
        result += bytes([tag * 16 + len(value)]) + value
    return result
