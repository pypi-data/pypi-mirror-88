from __future__ import annotations


class PcscServer:
    def __init__(self, sock, byteorder="="):
        self.sock = sock
        self.buf = bytearray()
        self._byteorder = byteorder

    async def _recv(self, n):
        while len(self.buf) < n:
            buf = await self.sock.receive_some(4096)
            if not buf:
                raise EOFError()
            self.buf.extend(buf)
        result = self.buf[:n]
        del self.buf[:n]
        return result

    async def recv_msg(self):
        size_cmd = await self._recv(8)
        size, cmd = struct.unpack(f"{self._byteorder}II", size_cmd)
        if size > 10000:
            raise ValueError(size)

        buf = await self._recv(size)
        return ProtocolMessage._subs[cmd].decode(buf, self._byteorder)

    async def send_msg(self, msg):
        await self.sock.send(msg.encoded_resp)
