import re
import asyncio
import asyncio.transports as transports
from collections.abc import Callable
from typing import Optional


class Scanner:
	def __init__(self, *args, **kwargs):
		assert 'loop' in kwargs, 'An asyncio loop needs to be provided to create a Scanner'
		assert 'callback' in kwargs, 'Semi useless to create a Scanner without a callback'
		set_value = lambda param_name, def_value: \
			def_value if param_name not in kwargs else kwargs.pop(param_name)
		self._ip = set_value('ip', '127.0.0.1')
		self._port = set_value('port', 1337)
		self._regex = set_value('regex', r'barcode=(\w+)')
		self._loop = kwargs.pop('loop')
		self._cb = kwargs.pop('callback')

	async def connect(self):
		# Todo implement reconnecting mechanism
		print("Connecting to ", self._ip, self._port)
		self.transport, self.protocol = await self._loop.create_connection(
			lambda: TcpClient(self._on_data(), self._on_connection())
			, host=self._ip
			, port=self._port)

	def _on_connection(self) -> Callable[bool]:
		def func(state: bool):
			print("Connected", state)
		return func

	def _on_data(self) -> Callable[str]:
		def func(data: str):
			barcode_match = re.search(self._regex, data)
			if barcode_match is None:
				print("Could not find barcode in data", data)
				print("Configured regular expression is", self._regex)
				return
			barcode_result = barcode_match.group(1)  # Todo is this the best way of parsing, given that the pattern is an argument
			if barcode_result is None:
				print("Regex is invalid, this validation should be moved to the constructor")
				return
			self._cb(barcode_result)
		return func


class TcpClient(asyncio.Protocol):
	def __init__(self, on_data: Callable[str], on_connect: Callable[bool]):
		super(TcpClient, self).__init__()
		self._on_data = on_data
		self._on_connect = on_connect

	def connection_made(self, transport: transports.BaseTransport) -> None:
		self._on_connect(True)

	def connection_lost(self, exc: Optional[Exception]) -> None:
		self._on_connect(False)

	def data_received(self, data: bytes) -> None:
		self._on_data(data.decode())
