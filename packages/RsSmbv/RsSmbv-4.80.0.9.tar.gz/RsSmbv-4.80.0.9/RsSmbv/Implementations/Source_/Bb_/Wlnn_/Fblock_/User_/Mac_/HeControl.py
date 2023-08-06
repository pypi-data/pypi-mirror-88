from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HeControl:
	"""HeControl commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("heControl", core, parent)

	def clone(self) -> 'HeControl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HeControl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def acontrol(self):
		"""acontrol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acontrol'):
			from .HeControl_.Acontrol import Acontrol
			self._acontrol = Acontrol(self._core, self._base)
		return self._acontrol

	@property
	def heIndicator(self):
		"""heIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_heIndicator'):
			from .HeControl_.HeIndicator import HeIndicator
			self._heIndicator = HeIndicator(self._core, self._base)
		return self._heIndicator

	def set(self, he_control: List[str], channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:HEControl \n
		Sets the value with the length of 4 bytes of the HE control field. \n
			:param he_control: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.list_to_csv_str(he_control)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:HEControl {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:HEControl \n
		Sets the value with the length of 4 bytes of the HE control field. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: he_control: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:HEControl?')
		return Conversions.str_to_str_list(response)
