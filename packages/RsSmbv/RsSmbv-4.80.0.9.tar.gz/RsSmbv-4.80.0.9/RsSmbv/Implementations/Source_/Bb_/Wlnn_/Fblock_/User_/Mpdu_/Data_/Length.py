from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("length", core, parent)

	def set(self, length: int, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MPDU<ST>:DATA:LENGth \n
		Determines the size of the data field in bytes. \n
			:param length: integer Range: 0 to 16384
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mpdu')"""
		param = Conversions.decimal_value_to_str(length)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MPDU{stream_cmd_val}:DATA:LENGth {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MPDU<ST>:DATA:LENGth \n
		Determines the size of the data field in bytes. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mpdu')
			:return: length: integer Range: 0 to 16384"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MPDU{stream_cmd_val}:DATA:LENGth?')
		return Conversions.str_to_int(response)
