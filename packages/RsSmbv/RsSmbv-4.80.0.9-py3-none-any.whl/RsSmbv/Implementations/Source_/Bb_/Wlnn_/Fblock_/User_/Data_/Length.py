from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("length", core, parent)

	def set(self, length: int, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:DATA:LENGth \n
		The command enters the size of the data field in bytes. For Data Length = 0, no data field will be generated for the case
		of a sounding frame. The maximum data length depends on the physical mode: In LEGACY mode, the maximum value is 4061
		Bytes. In MIXED MODE and GREEN FIELD, the maximum value is 65495 Bytes. The data length is related to the number of data
		symbols. Whenever the data length changes, the number of data symbols is updated and vice versa. \n
			:param length: integer Range: 0 to Max
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(length)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:DATA:LENGth {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:DATA:LENGth \n
		The command enters the size of the data field in bytes. For Data Length = 0, no data field will be generated for the case
		of a sounding frame. The maximum data length depends on the physical mode: In LEGACY mode, the maximum value is 4061
		Bytes. In MIXED MODE and GREEN FIELD, the maximum value is 65495 Bytes. The data length is related to the number of data
		symbols. Whenever the data length changes, the number of data symbols is updated and vice versa. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: length: integer Range: 0 to Max"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:DATA:LENGth?')
		return Conversions.str_to_int(response)
