from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("level", core, parent)

	def set(self, level: enums.GsmBursPowMode, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:LEVel \n
		The command defines the power control level of the selected slot. \n
			:param level: OFF| ATT| FULL OFF The slot is inactive. ATT The power is reduced by the amount defined using :BB:GSM:SLOT:ATT. FULL Full power as specified by the level setting.
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(level, enums.GsmBursPowMode)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:LEVel {param}')

	# noinspection PyTypeChecker
	def get(self, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> enums.GsmBursPowMode:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:LEVel \n
		The command defines the power control level of the selected slot. \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: level: OFF| ATT| FULL OFF The slot is inactive. ATT The power is reduced by the amount defined using :BB:GSM:SLOT:ATT. FULL Full power as specified by the level setting."""
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:LEVel?')
		return Conversions.str_to_scalar_enum(response, enums.GsmBursPowMode)
