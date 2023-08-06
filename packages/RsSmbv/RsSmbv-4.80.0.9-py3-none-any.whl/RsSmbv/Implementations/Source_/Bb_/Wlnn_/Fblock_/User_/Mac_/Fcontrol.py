from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fcontrol:
	"""Fcontrol commands group definition. 12 total commands, 11 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fcontrol", core, parent)

	def clone(self) -> 'Fcontrol':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fcontrol(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fds(self):
		"""fds commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fds'):
			from .Fcontrol_.Fds import Fds
			self._fds = Fds(self._core, self._base)
		return self._fds

	@property
	def mdata(self):
		"""mdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mdata'):
			from .Fcontrol_.Mdata import Mdata
			self._mdata = Mdata(self._core, self._base)
		return self._mdata

	@property
	def mfragments(self):
		"""mfragments commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mfragments'):
			from .Fcontrol_.Mfragments import Mfragments
			self._mfragments = Mfragments(self._core, self._base)
		return self._mfragments

	@property
	def order(self):
		"""order commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_order'):
			from .Fcontrol_.Order import Order
			self._order = Order(self._core, self._base)
		return self._order

	@property
	def pmanagement(self):
		"""pmanagement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmanagement'):
			from .Fcontrol_.Pmanagement import Pmanagement
			self._pmanagement = Pmanagement(self._core, self._base)
		return self._pmanagement

	@property
	def pversion(self):
		"""pversion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pversion'):
			from .Fcontrol_.Pversion import Pversion
			self._pversion = Pversion(self._core, self._base)
		return self._pversion

	@property
	def retry(self):
		"""retry commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_retry'):
			from .Fcontrol_.Retry import Retry
			self._retry = Retry(self._core, self._base)
		return self._retry

	@property
	def subType(self):
		"""subType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subType'):
			from .Fcontrol_.SubType import SubType
			self._subType = SubType(self._core, self._base)
		return self._subType

	@property
	def tds(self):
		"""tds commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tds'):
			from .Fcontrol_.Tds import Tds
			self._tds = Tds(self._core, self._base)
		return self._tds

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Fcontrol_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def wep(self):
		"""wep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wep'):
			from .Fcontrol_.Wep import Wep
			self._wep = Wep(self._core, self._base)
		return self._wep

	def set(self, fcontrol: List[str], channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:FCONtrol \n
		The command enters the value of the frame control field. The frame control field has a length of 2 bytes (16 bits) and is
		used to define the protocol version, the frame type, and its function, etc.. As an alternative, the individual bits can
		be set with the following commands. \n
			:param fcontrol: integer Range: #H0000,16 to #HFFFF,16
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.list_to_csv_str(fcontrol)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:FCONtrol {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:FCONtrol \n
		The command enters the value of the frame control field. The frame control field has a length of 2 bytes (16 bits) and is
		used to define the protocol version, the frame type, and its function, etc.. As an alternative, the individual bits can
		be set with the following commands. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: fcontrol: integer Range: #H0000,16 to #HFFFF,16"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:FCONtrol?')
		return Conversions.str_to_str_list(response)
