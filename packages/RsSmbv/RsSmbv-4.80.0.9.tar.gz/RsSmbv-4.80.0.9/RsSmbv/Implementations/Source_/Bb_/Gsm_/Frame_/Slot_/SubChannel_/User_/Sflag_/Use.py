from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Use:
	"""Use commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("use", core, parent)

	def set(self, use: bool, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:SFLag:USE \n
		The command enables or disables the use of Stealing Flags. If not used, the Stealing Flags bits are allocated to the DATA
		fields (only for Normal burst BB:GSM:SLOT:TYPE NORM) . \n
			:param use: 0| 1| OFF| ON
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.bool_to_str(use)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:SFLag:USE {param}')

	def get(self, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:SFLag:USE \n
		The command enables or disables the use of Stealing Flags. If not used, the Stealing Flags bits are allocated to the DATA
		fields (only for Normal burst BB:GSM:SLOT:TYPE NORM) . \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: use: 0| 1| OFF| ON"""
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:SFLag:USE?')
		return Conversions.str_to_bool(response)
