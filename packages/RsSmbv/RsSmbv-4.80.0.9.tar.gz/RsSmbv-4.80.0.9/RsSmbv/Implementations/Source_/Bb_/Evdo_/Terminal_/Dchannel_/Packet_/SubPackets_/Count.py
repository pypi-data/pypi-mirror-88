from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Count:
	"""Count commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("count", core, parent)

	def set(self, count: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:SUBPackets:[COUNt] \n
		(enabled for physical layer subtype 2 and for an access terminal working in traffic mode) Sets the number of subpackets
		to be sent. \n
			:param count: integer Range: 1 to 4
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')"""
		param = Conversions.decimal_value_to_str(count)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:SUBPackets:COUNt {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:SUBPackets:[COUNt] \n
		(enabled for physical layer subtype 2 and for an access terminal working in traffic mode) Sets the number of subpackets
		to be sent. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: count: integer Range: 1 to 4"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:SUBPackets:COUNt?')
		return Conversions.str_to_int(response)
