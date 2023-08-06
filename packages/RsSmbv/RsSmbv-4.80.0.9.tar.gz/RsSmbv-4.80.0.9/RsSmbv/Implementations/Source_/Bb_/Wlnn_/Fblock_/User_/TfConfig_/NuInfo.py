from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NuInfo:
	"""NuInfo commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nuInfo", core, parent)

	def set(self, no_user_info: int, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:NUINfo \n
		Sets the value bits of the user info field. You can configure the user info for up to 37 users with the command
		[:SOURce<hw>]:BB:WLNN:FBLock<ch>[:USER<di>]:TFConfig:NUINfo. \n
			:param no_user_info: 7 bits
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(no_user_info)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:TFConfig:NUINfo {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:NUINfo \n
		Sets the value bits of the user info field. You can configure the user info for up to 37 users with the command
		[:SOURce<hw>]:BB:WLNN:FBLock<ch>[:USER<di>]:TFConfig:NUINfo. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: no_user_info: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:TFConfig:NUINfo?')
		return Conversions.str_to_int(response)
