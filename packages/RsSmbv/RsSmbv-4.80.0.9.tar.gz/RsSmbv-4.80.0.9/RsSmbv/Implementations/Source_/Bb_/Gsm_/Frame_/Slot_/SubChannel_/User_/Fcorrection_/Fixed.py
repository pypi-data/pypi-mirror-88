from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fixed:
	"""Fixed commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fixed", core, parent)

	def clone(self) -> 'Fixed':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fixed(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Fixed_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	def set(self, fixed: enums.GsmBursFix, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:FCORrection:FIXed \n
		The command selects the content of the FIXED field for the Frequency Correction burst. There is a choice of two
		predefined sequences STANdard and COMPact and, if defined, a USER sequence (only for burst type selection
		BB:GSM:SLOT:TYPE FCORrection) . \n
			:param fixed: STANdard| COMPact| USER
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(fixed, enums.GsmBursFix)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:FCORrection:FIXed {param}')

	# noinspection PyTypeChecker
	def get(self, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> enums.GsmBursFix:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:FCORrection:FIXed \n
		The command selects the content of the FIXED field for the Frequency Correction burst. There is a choice of two
		predefined sequences STANdard and COMPact and, if defined, a USER sequence (only for burst type selection
		BB:GSM:SLOT:TYPE FCORrection) . \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: fixed: STANdard| COMPact| USER"""
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:FCORrection:FIXed?')
		return Conversions.str_to_scalar_enum(response, enums.GsmBursFix)
