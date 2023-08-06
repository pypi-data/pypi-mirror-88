from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.Cdma2KcodMode, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:CCODing:MODE \n
		Selects channel coding mode. For the traffic channels, this value is specific for the selected radio configuration. \n
			:param mode: OFF| COMPlete| NOINterleaving| OINTerleaving OFF Channel coding is deactivated. COMPlete The complete channel coding is performed. The channel coding procedure can slightly vary depending on channel type, frame length and data rate. OINTerleaving Except for the block interleaver, the whole channel coding procedure is carried out. In this mode, the frame structure and the convolutional coder of a receiver can be tested. NOINterleaving In this mode, only block interleaver is used for coding. This allows the deinterleaver in the receiver to be tested independently of the remaining (de-) coding process.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')"""
		param = Conversions.enum_scalar_to_str(mode, enums.Cdma2KcodMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:CCODing:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> enums.Cdma2KcodMode:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:CCODing:MODE \n
		Selects channel coding mode. For the traffic channels, this value is specific for the selected radio configuration. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: mode: OFF| COMPlete| NOINterleaving| OINTerleaving OFF Channel coding is deactivated. COMPlete The complete channel coding is performed. The channel coding procedure can slightly vary depending on channel type, frame length and data rate. OINTerleaving Except for the block interleaver, the whole channel coding procedure is carried out. In this mode, the frame structure and the convolutional coder of a receiver can be tested. NOINterleaving In this mode, only block interleaver is used for coding. This allows the deinterleaver in the receiver to be tested independently of the remaining (de-) coding process."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:CCODing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KcodMode)
