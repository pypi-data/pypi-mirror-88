from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlCount:
	"""AlCount commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alCount", core, parent)

	def set(self, alloc_count: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALCount \n
		Sets the number of scheduled allocations in the selected subframe. The maximum number of allocations that can be
		scheduled depends on the number of the selected resource blocks. \n
			:param alloc_count: integer Range: 0 to dynamic
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.decimal_value_to_str(alloc_count)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALCount {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALCount \n
		Sets the number of scheduled allocations in the selected subframe. The maximum number of allocations that can be
		scheduled depends on the number of the selected resource blocks. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: alloc_count: integer Range: 0 to dynamic"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALCount?')
		return Conversions.str_to_int(response)
