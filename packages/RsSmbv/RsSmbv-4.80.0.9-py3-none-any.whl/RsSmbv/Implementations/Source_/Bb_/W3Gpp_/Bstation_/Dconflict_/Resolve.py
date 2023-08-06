from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Resolve:
	"""Resolve commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("resolve", core, parent)

	def set(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:DCONflict:RESolve \n
		The command resolves existing domain conflicts by modifying the Channelization Codes of the affected channels. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:DCONflict:RESolve')

	def set_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:DCONflict:RESolve \n
		The command resolves existing domain conflicts by modifying the Channelization Codes of the affected channels. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:DCONflict:RESolve')
