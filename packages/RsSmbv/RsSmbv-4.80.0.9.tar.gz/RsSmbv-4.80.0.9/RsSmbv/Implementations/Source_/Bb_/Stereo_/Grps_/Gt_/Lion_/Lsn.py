from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lsn:
	"""Lsn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lsn", core, parent)

	def set(self, lsn: List[str], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:LION:LSN \n
		No command help available \n
			:param lsn: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')"""
		param = Conversions.list_to_csv_str(lsn)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:LION:LSN {param}')

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:LION:LSN \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:return: lsn: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:LION:LSN?')
		return Conversions.str_to_str_list(response)
