from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Count:
	"""Count commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("count", core, parent)

	def set(self, count: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:COUNt \n
		(enabled for an access terminal working in traffic mode) Sets the number of packets to be sent. The number of packets to
		be send depends on whether the parameter 'Infinite Packets' is enabled or disabled. If 'Infinite Packets'is enabled,
		there is no limit to the number of packets sent. If 'Infinite Packets' is disabled, the number of packets can be
		specified. In this case, the data channel will be switched off after the specified number of packets have been sent.
		Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only enabled for
		physical layer subtype 2. \n
			:param count: integer Range: 0 to 65536
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')"""
		param = Conversions.decimal_value_to_str(count)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:COUNt {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:COUNt \n
		(enabled for an access terminal working in traffic mode) Sets the number of packets to be sent. The number of packets to
		be send depends on whether the parameter 'Infinite Packets' is enabled or disabled. If 'Infinite Packets'is enabled,
		there is no limit to the number of packets sent. If 'Infinite Packets' is disabled, the number of packets can be
		specified. In this case, the data channel will be switched off after the specified number of packets have been sent.
		Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only enabled for
		physical layer subtype 2. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: count: integer Range: 0 to 65536"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:COUNt?')
		return Conversions.str_to_int(response)
