from __future__ import annotations

import logging
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any, AsyncGenerator, ByteString, Dict, Optional, Type, TypeVar

from anyio.abc import ByteStream

from .pcsc import PcscClient
from .pcsc.const import ReaderState
from .card.abstract import AbstractChipCard


@asynccontextmanager
async def async_null_context(result):
    yield result


T = TypeVar("T", bound=AbstractChipCard)

@asynccontextmanager
async def connect_chipcard(
    cls: Type[T],
    *,
    path: Optional[str] = None,
    sock: Optional[ByteStream] = None,
    reader_name: Optional[str] = None,
    reader_id: Optional[int] = None,
    atr: Optional[ByteString] = None,
    byteorder: str = "=",
    **kwargs: Dict[str, Any],
) -> AsyncGenerator[T, None]:
    """
    Open a chipcard that is compatible to cls.
    """

    if path and sock:
        raise TypeError("Cannot specify both path and sock")

    if sock:
        ctx = async_null_context(PcscClient(sock, byteorder))
    else:
        ctx = PcscClient.connect(path, byteorder)

    async with ctx as client, AsyncExitStack() as stack:
        usable_card = None
        wanted_state = ReaderState.NEGOTIABLE | ReaderState.POWERED | ReaderState.PRESENT
        for reader in await client.get_reader_state():
            if reader.reader_state & wanted_state != wanted_state:
                continue
            if reader_name is not None and reader_name != reader.name:
                continue
            if reader_id is not None and reader_id != reader.reader_id:
                continue
            if atr is not None and atr != reader.atr:
                continue
            card = cls(await stack.enter_async_context(reader.connect()))
            try:
                if not await card.is_usable(**kwargs):
                    card = None
                    await stack.aclose()
                    continue
            except Exception:
                logging.exception(f"Could not open card in {reader}")
                continue

            if usable_card:
                raise Exception(f"Multiple cards match: {usable_card.reader} {card.reader}")

            usable_card = card

        if not usable_card:
            raise Exception("No card matches the criteria")
        yield usable_card
