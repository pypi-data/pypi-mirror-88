from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpAddress:
	"""IpAddress commands group definition. 5 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipAddress", core, parent)

	def clone(self) -> 'IpAddress':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IpAddress(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def subnet(self):
		"""subnet commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subnet'):
			from .IpAddress_.Subnet import Subnet
			self._subnet = Subnet(self._core, self._base)
		return self._subnet

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.NetMode:
		"""SYSTem:COMMunicate:NETWork:IPADdress:MODE \n
		Selects manual or automatic setting of the IP address. \n
			:return: mode: AUTO| STATic
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:IPADdress:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.NetMode)

	def set_mode(self, mode: enums.NetMode) -> None:
		"""SYSTem:COMMunicate:NETWork:IPADdress:MODE \n
		Selects manual or automatic setting of the IP address. \n
			:param mode: AUTO| STATic
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.NetMode)
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:IPADdress:MODE {param}')

	def get_dns(self) -> str:
		"""SYSTem:COMMunicate:NETWork:[IPADdress]:DNS \n
		Determines or queries the network DNS server to resolve the name. \n
			:return: dns: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:IPADdress:DNS?')
		return trim_str_response(response)

	def set_dns(self, dns: str) -> None:
		"""SYSTem:COMMunicate:NETWork:[IPADdress]:DNS \n
		Determines or queries the network DNS server to resolve the name. \n
			:param dns: string
		"""
		param = Conversions.value_to_quoted_str(dns)
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:IPADdress:DNS {param}')

	def get_gateway(self) -> str:
		"""SYSTem:COMMunicate:NETWork:[IPADdress]:GATeway \n
		Sets the IP address of the default gateway. \n
			:return: gateway: string Range: 0.0.0.0 to ff.ff.ff.ff
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:IPADdress:GATeway?')
		return trim_str_response(response)

	def set_gateway(self, gateway: str) -> None:
		"""SYSTem:COMMunicate:NETWork:[IPADdress]:GATeway \n
		Sets the IP address of the default gateway. \n
			:param gateway: string Range: 0.0.0.0 to ff.ff.ff.ff
		"""
		param = Conversions.value_to_quoted_str(gateway)
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:IPADdress:GATeway {param}')

	def get_value(self) -> str:
		"""SYSTem:COMMunicate:NETWork:IPADdress \n
		Sets the IP address. \n
			:return: ip_address: string Range: 0.0.0.0. to ff.ff.ff.ff
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:IPADdress?')
		return trim_str_response(response)

	def set_value(self, ip_address: str) -> None:
		"""SYSTem:COMMunicate:NETWork:IPADdress \n
		Sets the IP address. \n
			:param ip_address: string Range: 0.0.0.0. to ff.ff.ff.ff
		"""
		param = Conversions.value_to_quoted_str(ip_address)
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:IPADdress {param}')
