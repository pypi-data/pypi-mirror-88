from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nid:
	"""Nid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nid", core, parent)

	def set(self, epdcch_id: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, direction=repcap.Direction.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:EPDCch:CELL<ST>:SET<DIR>:NID \n
		Sets the identifier nEPDCCHID,m used to calculate the UE-specific scrambling sequence. \n
			:param epdcch_id: integer Range: 0 to 503
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param direction: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')"""
		param = Conversions.decimal_value_to_str(epdcch_id)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		direction_cmd_val = self._base.get_repcap_cmd_value(direction, repcap.Direction)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:EPDCch:CELL{stream_cmd_val}:SET{direction_cmd_val}:NID {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, direction=repcap.Direction.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:EPDCch:CELL<ST>:SET<DIR>:NID \n
		Sets the identifier nEPDCCHID,m used to calculate the UE-specific scrambling sequence. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param direction: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: epdcch_id: integer Range: 0 to 503"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		direction_cmd_val = self._base.get_repcap_cmd_value(direction, repcap.Direction)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:EPDCch:CELL{stream_cmd_val}:SET{direction_cmd_val}:NID?')
		return Conversions.str_to_int(response)
