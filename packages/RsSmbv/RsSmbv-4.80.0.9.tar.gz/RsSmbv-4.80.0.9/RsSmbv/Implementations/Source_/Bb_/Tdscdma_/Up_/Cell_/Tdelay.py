from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdelay:
	"""Tdelay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdelay", core, parent)

	def set(self, tdelay: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:TDELay \n
		Sets the time shift of the selected cell compared to cell 1; the time delay of cell 1 is 0. \n
			:param tdelay: integer Range: 0 to 19200, Unit: chip
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(tdelay)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:TDELay {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:TDELay \n
		Sets the time shift of the selected cell compared to cell 1; the time delay of cell 1 is 0. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: tdelay: integer Range: 0 to 19200, Unit: chip"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:TDELay?')
		return Conversions.str_to_int(response)
