from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def set(self, ul_bb_delay: int, rowIx=repcap.RowIx.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:APMap:ROW<BBID>:DELay \n
		No command help available \n
			:param ul_bb_delay: No help available
			:param rowIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(ul_bb_delay)
		rowIx_cmd_val = self._base.get_repcap_cmd_value(rowIx, repcap.RowIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:APMap:ROW{rowIx_cmd_val}:DELay {param}')

	def get(self, rowIx=repcap.RowIx.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:APMap:ROW<BBID>:DELay \n
		No command help available \n
			:param rowIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: ul_bb_delay: No help available"""
		rowIx_cmd_val = self._base.get_repcap_cmd_value(rowIx, repcap.RowIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:APMap:ROW{rowIx_cmd_val}:DELay?')
		return Conversions.str_to_int(response)
