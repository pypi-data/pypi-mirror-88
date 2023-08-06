from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Address:
	"""Address commands group definition. 2 total commands, 1 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("address", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Address':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Address(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Address_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def set(self, address: List[str], channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:ADDRess<ST> \n
		The command enters the value of the address fields 1 ... 4. Exactly 48 bits must be entered. Each address is 6 bytes (48
		bit) long. The addresses can be entered in hexadecimal form in the entry field of each address field.
		The least significant byte (LSB) is in left notation. \n
			:param address: integer Range: #H000000000000,48 to #HFFFFFFFFFFFF,48
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Address')"""
		param = Conversions.list_to_csv_str(address)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:ADDRess{stream_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:ADDRess<ST> \n
		The command enters the value of the address fields 1 ... 4. Exactly 48 bits must be entered. Each address is 6 bytes (48
		bit) long. The addresses can be entered in hexadecimal form in the entry field of each address field.
		The least significant byte (LSB) is in left notation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Address')
			:return: address: integer Range: #H000000000000,48 to #HFFFFFFFFFFFF,48"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:ADDRess{stream_cmd_val}?')
		return Conversions.str_to_str_list(response)
