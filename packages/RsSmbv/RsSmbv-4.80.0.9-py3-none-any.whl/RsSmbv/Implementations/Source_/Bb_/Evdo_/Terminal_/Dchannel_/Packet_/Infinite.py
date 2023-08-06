from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Infinite:
	"""Infinite commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("infinite", core, parent)

	def set(self, infinite: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:INFinite \n
		(enabled for an access terminal working in traffic mode) Enables or disables sending an unlimited number of packets. The
		parameter 'Number of Packets to be Send' depends on whether the parameter 'Infinite Packets' is enabled or disabled.
		If 'Infinite Packets' is enabled, there is no limit to the number of packets sent. If 'Infinite Packets' is disabled, the
		number of packets can be specified. Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third
		subframe, is only enabled for physical layer subtype 2. \n
			:param infinite: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')"""
		param = Conversions.bool_to_str(infinite)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:INFinite {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:INFinite \n
		(enabled for an access terminal working in traffic mode) Enables or disables sending an unlimited number of packets. The
		parameter 'Number of Packets to be Send' depends on whether the parameter 'Infinite Packets' is enabled or disabled.
		If 'Infinite Packets' is enabled, there is no limit to the number of packets sent. If 'Infinite Packets' is disabled, the
		number of packets can be specified. Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third
		subframe, is only enabled for physical layer subtype 2. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: infinite: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:INFinite?')
		return Conversions.str_to_bool(response)
