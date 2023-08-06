from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Magnitude:
	"""Magnitude commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("magnitude", core, parent)

	def set(self, prs_ap_magn: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default, column=repcap.Column.Default, row=repcap.Row.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:APMap:COL<GR>:ROW<USER>:MAGNitude \n
		Sets the mapping of the antenna ports (AP) for the PRS resource, if cylindrical coordinates are used. \n
			:param prs_ap_magn: float Range: 0 to 360
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(prs_ap_magn)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:APMap:COL{column_cmd_val}:ROW{row_cmd_val}:MAGNitude {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default, column=repcap.Column.Default, row=repcap.Row.Default) -> float:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:APMap:COL<GR>:ROW<USER>:MAGNitude \n
		Sets the mapping of the antenna ports (AP) for the PRS resource, if cylindrical coordinates are used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: prs_ap_magn: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:APMap:COL{column_cmd_val}:ROW{row_cmd_val}:MAGNitude?')
		return Conversions.str_to_float(response)
