from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Network:
	"""Network commands group definition. 12 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("network", core, parent)

	def clone(self) -> 'Network':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Network(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ipAddress(self):
		"""ipAddress commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_ipAddress'):
			from .Network_.IpAddress import IpAddress
			self._ipAddress = IpAddress(self._core, self._base)
		return self._ipAddress

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_restart'):
			from .Network_.Restart import Restart
			self._restart = Restart(self._core, self._base)
		return self._restart

	@property
	def common(self):
		"""common commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_common'):
			from .Network_.Common import Common
			self._common = Common(self._core, self._base)
		return self._common

	def get_mac_address(self) -> str:
		"""SYSTem:COMMunicate:NETWork:MACaddress \n
		Queries the MAC address of the network adapter. This is a password-protected function. Unlock the protection level 1 to
		access it. See SYSTem. \n
			:return: mac_address: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:MACaddress?')
		return trim_str_response(response)

	def set_mac_address(self, mac_address: str) -> None:
		"""SYSTem:COMMunicate:NETWork:MACaddress \n
		Queries the MAC address of the network adapter. This is a password-protected function. Unlock the protection level 1 to
		access it. See SYSTem. \n
			:param mac_address: string
		"""
		param = Conversions.value_to_quoted_str(mac_address)
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:MACaddress {param}')

	def get_resource(self) -> str:
		"""SYSTem:COMMunicate:NETWork:RESource \n
		Queries the visa resource string for Ethernet instruments. \n
			:return: resource: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:RESource?')
		return trim_str_response(response)

	def get_status(self) -> bool:
		"""SYSTem:COMMunicate:NETWork:STATus \n
		Queries the network configuration state. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:STATus?')
		return Conversions.str_to_bool(response)
