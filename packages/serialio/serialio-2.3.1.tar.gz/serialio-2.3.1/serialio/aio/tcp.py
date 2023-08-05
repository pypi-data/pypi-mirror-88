import logging
import urllib.parse

import sockio.aio

from .base import LF, SerialBase, SerialException, assert_open, async_assert_open


log = logging.getLogger("serialio.tcp.aio")


class Serial(SerialBase):
    """Serial port implementation for plain tcp sockets."""

    def __init__(self, *args, **kwargs):
        self.logger = log
        super().__init__(*args, **kwargs)
        host, port = self.from_url(self._port)
        self._socket = sockio.aio.TCP(
            host,
            port,
            eol=self._eol,
            timeout=self._timeout,
            auto_reconnect=self._auto_reconnect,
        )

    @property
    def is_open(self):
        return self._socket.is_open

    @property
    def in_waiting(self):
        return self._socket.in_waiting

    async def _reconfigure_port(self):
        pass

    @staticmethod
    def from_url(url):
        """\
        extract host and port from an URL string, other settings are extracted
        an stored in instance
        """
        parts = urllib.parse.urlsplit(url)
        try:
            if not 0 <= parts.port < 65536:
                raise ValueError("port not in range 0...65535")
        except ValueError as e:
            raise SerialException(
                "expected a string in the form "
                '"[serial-tcp://]<host>:<port>": {}'.format(e)
            )
        return (parts.hostname, parts.port)

    async def open(self):
        await self._socket.open()

    async def close(self):
        await self._socket.close()

    async def read(self, size=1):
        return await self._socket.read(size)

    async def readline(self, eol=None):
        return await self._socket.readline(eol=eol)

    async def readuntil(self, separator=LF):
        return await self._socket.readuntil(separator)

    async def read_all(self):
        return await self._socket.readbuffer()

    async def write(self, data):
        return await self._socket.write(data)

    async def reset_input_buffer(self):
        self._socket.reset_input_buffer()

    async def reset_output_buffer(self):
        # ignored in raw tcp socket
        pass

    async def send_break(self, duration=0.25):
        # ignored in raw tcp socket
        pass

    # Extra interface not provided by serial.Serial

    async def readlines(self, n, eol=None):
        return await self._socket.readlines(n, eol=eol)

    async def writelines(self, lines):
        return await self._socket.writelines(lines)

    async def write_readline(self, data, eol=None):
        return await self._socket.write_readline(data, eol=eol)

    async def write_readlines(self, data, n, eol=None):
        return await self._socket.write_readlines(data, n, eol=eol)

    async def writelines_readlines(self, lines, n=None, eol=None):
        return await self._socket.writelines_readlines(lines, n=n, eol=eol)
