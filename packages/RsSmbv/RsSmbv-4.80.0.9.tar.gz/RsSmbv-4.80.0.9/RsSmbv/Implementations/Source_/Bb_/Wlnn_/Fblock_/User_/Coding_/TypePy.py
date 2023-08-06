from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.WlannFbCodType, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:CODing:TYPE \n
		Selects the channel coding. \n
			:param type_py: OFF| BCC
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.WlannFbCodType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:CODing:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> enums.WlannFbCodType:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:CODing:TYPE \n
		Selects the channel coding. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: type_py: OFF| BCC"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:CODing:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbCodType)
