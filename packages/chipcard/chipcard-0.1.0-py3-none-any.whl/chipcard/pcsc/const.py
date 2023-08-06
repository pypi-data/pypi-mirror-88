"""
Constants used by PCSC lite.

Based on:
    - https://salsa.debian.org/rousseau/PCSC/-/blob/master/src/PCSC/pcsclite.h.in
    - https://salsa.debian.org/rousseau/PCSC/-/blob/master/src/winscard_msg.h

/*
 * MUSCLE SmartCard Development ( https://pcsclite.apdu.fr/ )
 *
 * Copyright (C) 1999-2004
 *  David Corcoran <corcoran@musclecard.com>
 * Copyright (C) 2002-2011
 *  Ludovic Rousseau <ludovic.rousseau@free.fr>
 * Copyright (C) 2005
 *  Martin Paljak <martin@paljak.pri.ee>
 *
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
"""

from __future__ import annotations

from enum import IntEnum, IntFlag

# Maximum number of readers that can be connected
MAX_READERS_CONTEXTS = 16

# Maximum receive buffer size
MAX_BUFFER_SIZE_EXTENDED = 4 + 3 + (1 << 16) + 3 + 2

# Maximum length of reader name
MAX_READERNAME = 128

SIZEOF_SCARD_IO_REQUEST = 16


class ReaderState(IntFlag):
    """
    """

    # No reader present
    NOREADER = 0x0000

    # Unknown state
    UNKNOWN = 0x0001

    # Card is absent
    ABSENT = 0x0002

    # Card is present
    PRESENT = 0x0004

    # Card not powered
    SWALLOWED = 0x0008

    # Card is powered
    POWERED = 0x0010

    # Ready for PTS
    NEGOTIABLE = 0x0020

    # PTS has been set
    SPECIFIC = 0x0040


class MsgCommand(IntEnum):
    """
    """

    ESTABLISH_CONTEXT = 0x01
    RELEASE_CONTEXT = 0x02
    LIST_READERS = 0x03
    CONNECT = 0x04
    RECONNECT = 0x05
    DISCONNECT = 0x06
    BEGIN_TRANSACTION = 0x07
    END_TRANSACTION = 0x08
    TRANSMIT = 0x09
    CONTROL = 0x0A
    STATUS = 0x0B
    GET_STATUS_CHANGE = 0x0C
    CANCEL = 0x0D
    CANCEL_TRANSACTION = 0x0E
    GET_ATTRIB = 0x0F
    SET_ATTRIB = 0x10
    VERSION = 0x11
    GET_READERS_STATE = 0x12
    WAIT_READER_STATE_CHANGE = 0x13
    STOP_WAITING_READER_STATE_CHANGE = 0x14


class ScardScope(IntEnum):
    """
    """

    # Scope is user space
    USER = 0x00

    # Scope is terminal
    TERMINAL = 0x01

    # Scope is system
    SYSTEM = 0x02

    # Scope is global
    GLOBAL = 0x03


class ScardShare(IntEnum):
    """
    """

    # Share mode not set
    UNKNOWN = 0x00

    # Exclusive mode only
    EXCLUSIVE = 0x01

    # Shared mode only
    SHARED = 0x02

    # Raw mode only
    DIRECT = 0x03


class ScardSharing(IntEnum):
    """
    """

    # Is in exclusive mode
    EXCLUSIVE_CONTEXT = -1

    # Not used
    NO_CONTEXT = 0

    # Only one application is using it
    LAST_CONTEXT = 1


class ScardProtocol(IntFlag):
    """
    """

    # Protocol not set
    UNDEFINED = 0x00

    # T=0 active protocol
    T0 = 0x01

    # T=1 active protocol
    T1 = 0x02

    # Raw active protocol
    RAW = 0x04

    # T=15 protocol
    T15 = 0x08

    # T0 or T1; IFD determines protocol
    ANY = 0x03


class Disposition(IntEnum):
    # Do nothing on close
    LEAVE = 0x00

    # Reset on close
    RESET = 0x01

    # Power down on close
    UNPOWER = 0x02

    # Eject on close
    EJECT = 0x03
