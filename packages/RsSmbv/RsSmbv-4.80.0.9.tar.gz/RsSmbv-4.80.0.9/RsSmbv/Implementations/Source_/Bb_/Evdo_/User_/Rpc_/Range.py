from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Range:
	"""Range commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("range", core, parent)

	def set(self, range_py: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RPC:RANGe \n
		Sets the number of Reverse Power Control (RPC) bits sent in each direction when the 'RPC Mode = Range'. The specified
		value is used immediately. \n
			:param range_py: integer Range: 1 to 256
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(range_py)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RPC:RANGe {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RPC:RANGe \n
		Sets the number of Reverse Power Control (RPC) bits sent in each direction when the 'RPC Mode = Range'. The specified
		value is used immediately. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: range_py: integer Range: 1 to 256"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RPC:RANGe?')
		return Conversions.str_to_int(response)
