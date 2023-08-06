from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Icomponent:
	"""Icomponent commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("icomponent", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, column=repcap.Column.Default) -> float:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SMAPping:ROW<ST>:COL<DIR>:I \n
		Queries the time shift value of element I of the selected row and column of the spatial transmit matrix. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:return: ipart: float"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SMAPping:ROW{stream_cmd_val}:COL{column_cmd_val}:I?')
		return Conversions.str_to_float(response)
