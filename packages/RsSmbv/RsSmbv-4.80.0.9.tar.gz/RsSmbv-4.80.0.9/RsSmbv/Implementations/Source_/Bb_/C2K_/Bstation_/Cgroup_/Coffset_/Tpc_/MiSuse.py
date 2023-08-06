from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MiSuse:
	"""MiSuse commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("miSuse", core, parent)

	def set(self, mis_use: bool, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:TPC:MISuse \n
		The command activates 'mis-' use of the power control bits of the selected F-DCCH or F- FCH for controlling the channel
		powers of these channels. Power control is available for sub channel types F-DCCH and F-FCH. F-DCCH is only generated for
		radio configurations 3, 4 and 5. The bit pattern (see commands BB:C2K:BSTation<n>:CGRoup<n>:COFFset<n>:TPC...) of the
		power control bits of each channel is used to control the channel power. A '1' leads to an increase of channel powers, a
		'0' to a reduction of channel powers. Channel power is limited to the range 0 dB to -80 dB. The step width of the change
		is defined with the command method RsSmbv.Source.Bb.C2K.Bstation.Cgroup.Coffset.Tpc.Pstep.set. For the traffic channels,
		this value is specific for the selected radio configuration. \n
			:param mis_use: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')"""
		param = Conversions.bool_to_str(mis_use)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:TPC:MISuse {param}')

	def get(self, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:TPC:MISuse \n
		The command activates 'mis-' use of the power control bits of the selected F-DCCH or F- FCH for controlling the channel
		powers of these channels. Power control is available for sub channel types F-DCCH and F-FCH. F-DCCH is only generated for
		radio configurations 3, 4 and 5. The bit pattern (see commands BB:C2K:BSTation<n>:CGRoup<n>:COFFset<n>:TPC...) of the
		power control bits of each channel is used to control the channel power. A '1' leads to an increase of channel powers, a
		'0' to a reduction of channel powers. Channel power is limited to the range 0 dB to -80 dB. The step width of the change
		is defined with the command method RsSmbv.Source.Bb.C2K.Bstation.Cgroup.Coffset.Tpc.Pstep.set. For the traffic channels,
		this value is specific for the selected radio configuration. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: mis_use: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:TPC:MISuse?')
		return Conversions.str_to_bool(response)
