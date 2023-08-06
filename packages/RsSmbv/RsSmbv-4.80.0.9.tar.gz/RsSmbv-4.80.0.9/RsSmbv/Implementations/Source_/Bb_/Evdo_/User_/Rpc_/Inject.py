from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Inject:
	"""Inject commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inject", core, parent)

	def set(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RPC:INJect \n
		Enables sending of user defined Reverse Power Control (RPC) pattern at the end of the current RPC mode. The former RPC
		mode is restart at the end of the pattern transmission. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RPC:INJect')

	def set_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RPC:INJect \n
		Enables sending of user defined Reverse Power Control (RPC) pattern at the end of the current RPC mode. The former RPC
		mode is restart at the end of the pattern transmission. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RPC:INJect')
