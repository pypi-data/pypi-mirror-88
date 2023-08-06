from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BurstIndex:
	"""BurstIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("burstIndex", core, parent)

	def set(self, burst_index: List[int], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:MFRame:SLOT<ST>:BURStindex \n
		No command help available \n
			:param burst_index: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')"""
		param = Conversions.list_to_csv_str(burst_index)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:MFRame:SLOT{stream_cmd_val}:BURStindex {param}')

	def get(self, stream=repcap.Stream.Default) -> List[int]:
		"""[SOURce<HW>]:BB:GSM:MFRame:SLOT<ST>:BURStindex \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:return: burst_index: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_bin_or_ascii_int_list(f'SOURce<HwInstance>:BB:GSM:MFRame:SLOT{stream_cmd_val}:BURStindex?')
		return response
