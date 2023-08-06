from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Control:
	"""Control commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("control", core, parent)

	def set(self, nav_msg_control: enums.NavMsgCtrl, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SIGNal:L2Band:L2C:DATA:NMESsage:CONTrol \n
		Defines whether the navigation message parameters can be changed or not. \n
			:param nav_msg_control: OFF| EDIT| AUTO | OFF| EDIT| AUTO OFF Disables sending the navigation message. EDIT Enables configuration of the navigation message. AUTO Navigation message is generated automatically.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.enum_scalar_to_str(nav_msg_control, enums.NavMsgCtrl)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SIGNal:L2Band:L2C:DATA:NMESsage:CONTrol {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.NavMsgCtrl:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SIGNal:L2Band:L2C:DATA:NMESsage:CONTrol \n
		Defines whether the navigation message parameters can be changed or not. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: nav_msg_control: OFF| EDIT| AUTO | OFF| EDIT| AUTO OFF Disables sending the navigation message. EDIT Enables configuration of the navigation message. AUTO Navigation message is generated automatically."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SIGNal:L2Band:L2C:DATA:NMESsage:CONTrol?')
		return Conversions.str_to_scalar_enum(response, enums.NavMsgCtrl)
