from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bit:
	"""Bit commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bit", core, parent)

	def set(self, bit: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RPC:ZONE<CH>:BIT \n
		The Reverse Power Control (RPC) pattern is defined in form of table with four zones (zone 0 .. 3) . For each zone, a bit
		and a count can be defined. This parameter defines the RPC bits sent within the specific zone of the RPC Pattern. \n
			:param bit: 0| 1 Range: 0 to 1
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Zone')"""
		param = Conversions.decimal_value_to_str(bit)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RPC:ZONE{channel_cmd_val}:BIT {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RPC:ZONE<CH>:BIT \n
		The Reverse Power Control (RPC) pattern is defined in form of table with four zones (zone 0 .. 3) . For each zone, a bit
		and a count can be defined. This parameter defines the RPC bits sent within the specific zone of the RPC Pattern. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Zone')
			:return: bit: 0| 1 Range: 0 to 1"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RPC:ZONE{channel_cmd_val}:BIT?')
		return Conversions.str_to_int(response)
