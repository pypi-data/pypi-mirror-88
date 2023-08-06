from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Etsc:
	"""Etsc commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("etsc", core, parent)

	def clone(self) -> 'Etsc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Etsc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .Etsc_.User import User
			self._user = User(self._core, self._base)
		return self._user

	def set(self, etsc: enums.GsmBursTscExt, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:ETSC \n
		The command selects an extended training sequence for the Synchronization burst. There is a choice of three predefined
		sequences STANdard | CTS | COMPact and, if defined, a USER sequence (only for selection of burst type BB:GSM:SLOT:TYPE
		SYNC) . \n
			:param etsc: STANdard| CTS| COMPact| USER
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(etsc, enums.GsmBursTscExt)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:ETSC {param}')

	# noinspection PyTypeChecker
	def get(self, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> enums.GsmBursTscExt:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:ETSC \n
		The command selects an extended training sequence for the Synchronization burst. There is a choice of three predefined
		sequences STANdard | CTS | COMPact and, if defined, a USER sequence (only for selection of burst type BB:GSM:SLOT:TYPE
		SYNC) . \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: etsc: STANdard| CTS| COMPact| USER"""
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:ETSC?')
		return Conversions.str_to_scalar_enum(response, enums.GsmBursTscExt)
