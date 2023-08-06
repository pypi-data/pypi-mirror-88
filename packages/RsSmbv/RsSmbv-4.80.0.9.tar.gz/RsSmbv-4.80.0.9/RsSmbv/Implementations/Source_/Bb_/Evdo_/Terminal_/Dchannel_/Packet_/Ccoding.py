from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccoding", core, parent)

	def set(self, ccoding: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:CCODing \n
		(enabled for an access terminal working in traffic mode) Activates or deactivates channel coding, including scrambling,
		turbo encoding and channel interleaving. \n
			:param ccoding: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')"""
		param = Conversions.bool_to_str(ccoding)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:CCODing {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:CCODing \n
		(enabled for an access terminal working in traffic mode) Activates or deactivates channel coding, including scrambling,
		turbo encoding and channel interleaving. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: ccoding: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:CCODing?')
		return Conversions.str_to_bool(response)
