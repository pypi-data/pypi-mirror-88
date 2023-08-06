from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Staid:
	"""Staid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("staid", core, parent)

	def set(self, sta_id: int, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:USER<DI>:STAid \n
		Sets the station ID for the current user, the 11 least significant bits of the association identifier (AID) . \n
			:param sta_id: integer Range: 0 to 2047
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(sta_id)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:STAid {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:USER<DI>:STAid \n
		Sets the station ID for the current user, the 11 least significant bits of the association identifier (AID) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: sta_id: integer Range: 0 to 2047"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:STAid?')
		return Conversions.str_to_int(response)
