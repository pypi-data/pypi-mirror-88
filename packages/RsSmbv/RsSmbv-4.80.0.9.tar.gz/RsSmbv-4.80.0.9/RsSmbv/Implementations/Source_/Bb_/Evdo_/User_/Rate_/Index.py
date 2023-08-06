from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Index:
	"""Index commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("index", core, parent)

	def set(self, index: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RATE:INDex \n
		Determines the rate index. Note: Selected rate becomes effective at the beginning of the next packet transmitted to the
		selected user. \n
			:param index: integer Range: 1 to 12 (physical layer subtype 0&1) , 1 to 14 (physical layer subtype 2) , 1 to 28 (physical layer subtype 3)
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(index)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RATE:INDex {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RATE:INDex \n
		Determines the rate index. Note: Selected rate becomes effective at the beginning of the next packet transmitted to the
		selected user. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: index: integer Range: 1 to 12 (physical layer subtype 0&1) , 1 to 14 (physical layer subtype 2) , 1 to 28 (physical layer subtype 3)"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RATE:INDex?')
		return Conversions.str_to_int(response)
