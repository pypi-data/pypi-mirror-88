from __future__ import annotations
from .abstract import AbstractChipCard


class OpenPgpCard(AbstractChipCard):
    ATR_V1 = bytes.fromhex("3bda18ff81b1fe751f030031c573c001400090000c")
    ATR_V2 = bytes.fromhex("3bda18ff81b1fe751f030031f573c001600090001c")

    async def is_usable(self):
        return self.card.reader.atr in {self.ATR_V1, self.ATR_V2}

    async def get_random(self, count: int) -> bytes:
        return (await self.get_challenge(count)).data

    async def select_openpgp(self, exp=0) -> FileControlInformation:
        """
        Returns:
            FCI
        """
        return await self.ins_select(0, 4, 0, b'\xd2\x76\x00\x01\x24\x01', exp)

    async def unlock_pw1_sign(self, password: ByteString) -> None:
        await self.ins_verify_password(0, 0, 0x81, password)

    async def unlock_pw1_all(self, password: ByteString) -> None:
        await self.ins_verify_password(0, 0, 0x82, password)

    async def unlock_pw3(self, password: ByteString) -> None:
        await self.ins_verify_password(0, 0, 0x83, password)

    async def reinitialize(self) -> None:
        await self.ins_terminate_df(0)

    async def activate(self) -> None:
        await self.ins_activate_current_file(0)

    async def read_tag(self, tag: int) -> bytes:
        return await self.ins_get_data(0, tag >> 8, tag & 0xff)

    async def read_next_tag(self, tag: int) -> bytes:
        return await self.ins_get_next_data(0, tag >> 8, tag & 0xff)

    async def write_tag(self, tag: int, data: ByteString) -> None:
        return await self.ins_put_data(0, tag >> 8, tag & 0xff, data)

    async def compute_digital_signature(self, data: ByteString) -> bytes:
        resp = await self.send(0x00, 0x2A, 0x9E, 0x9A, data, 65536)
        return resp.data

#   select_data
#   get_data
#   get_next_data
#   verify
#   change_reference_data
#   reset_retry_counter
#   put_data
#   generate_asymmetric_keypair
#   decipher
#   encipher
#   internal_authenticate
#   get_response
#   get_challenge
#   terminate_df
#   activate_file
#   manage_security_environment
#   generate_attestation
