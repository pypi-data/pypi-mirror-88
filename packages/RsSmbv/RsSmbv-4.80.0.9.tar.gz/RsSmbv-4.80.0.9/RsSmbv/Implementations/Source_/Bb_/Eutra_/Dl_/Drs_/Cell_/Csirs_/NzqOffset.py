from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NzqOffset:
	"""NzqOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nzqOffset", core, parent)

	def set(self, non_zero_pq_offs: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:CSIRs<ST>:NZQoffset \n
		Sets the Q-offset. \n
			:param non_zero_pq_offs: -24| -22| -20| -18| -16| -14| -12| -10| -8| -6| -5| -4| -3| -2| -1| 0| 1| 2| 3| 4| 5| 6| 8| 10| 12| 14| 16| 18| 20| 22| 24 Positive values outside the permitted discrete values are rounded down; negative values are rounded up.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Csirs')"""
		param = Conversions.decimal_value_to_str(non_zero_pq_offs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:CSIRs{stream_cmd_val}:NZQoffset {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:CSIRs<ST>:NZQoffset \n
		Sets the Q-offset. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Csirs')
			:return: non_zero_pq_offs: -24| -22| -20| -18| -16| -14| -12| -10| -8| -6| -5| -4| -3| -2| -1| 0| 1| 2| 3| 4| 5| 6| 8| 10| 12| 14| 16| 18| 20| 22| 24 Positive values outside the permitted discrete values are rounded down; negative values are rounded up."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:CSIRs{stream_cmd_val}:NZQoffset?')
		return Conversions.str_to_int(response)
