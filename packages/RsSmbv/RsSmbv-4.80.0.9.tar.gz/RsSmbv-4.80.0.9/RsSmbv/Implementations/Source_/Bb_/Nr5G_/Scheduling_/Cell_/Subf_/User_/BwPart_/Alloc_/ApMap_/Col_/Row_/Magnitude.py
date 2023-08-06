from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal import Conversions
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Magnitude:
	"""Magnitude commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("magnitude", core, parent)

	def set(self, apmap_data_magn: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, column=repcap.Column.Default, row=repcap.Row.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:APMap:COL<S2US>:ROW<S3US>:MAGNitude \n
		Defines the mapping of the antenna ports to the physical antennas, cylindrical mapping coordinates are used. \n
			:param apmap_data_magn: float Range: 0 to 1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(apmap_data_magn)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:APMap:COL{column_cmd_val}:ROW{row_cmd_val}:MAGNitude {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, column=repcap.Column.Default, row=repcap.Row.Default) -> float:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:APMap:COL<S2US>:ROW<S3US>:MAGNitude \n
		Defines the mapping of the antenna ports to the physical antennas, cylindrical mapping coordinates are used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: apmap_data_magn: float Range: 0 to 1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:APMap:COL{column_cmd_val}:ROW{row_cmd_val}:MAGNitude?')
		return Conversions.str_to_float(response)
