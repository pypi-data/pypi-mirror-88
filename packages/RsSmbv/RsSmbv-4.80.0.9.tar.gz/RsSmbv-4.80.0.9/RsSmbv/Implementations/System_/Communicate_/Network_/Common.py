from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Common:
	"""Common commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("common", core, parent)

	def get_domain(self) -> str:
		"""SYSTem:COMMunicate:NETWork:[COMMon]:DOMain \n
		Determines the primary suffix of the network domain. \n
			:return: domain: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:COMMon:DOMain?')
		return trim_str_response(response)

	def set_domain(self, domain: str) -> None:
		"""SYSTem:COMMunicate:NETWork:[COMMon]:DOMain \n
		Determines the primary suffix of the network domain. \n
			:param domain: string
		"""
		param = Conversions.value_to_quoted_str(domain)
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:COMMon:DOMain {param}')

	def get_hostname(self) -> str:
		"""SYSTem:COMMunicate:NETWork:[COMMon]:HOSTname \n
		Sets an individual hostname for the vector signal generator. Note:We recommend that you do not change the hostname to
		avoid problems with the network connection. If you change the hostname, be sure to use a unique name.
		This is a password-protected function. Unlock the protection level 1 to access it. See SYSTem. \n
			:return: hostname: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:COMMon:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, hostname: str) -> None:
		"""SYSTem:COMMunicate:NETWork:[COMMon]:HOSTname \n
		Sets an individual hostname for the vector signal generator. Note:We recommend that you do not change the hostname to
		avoid problems with the network connection. If you change the hostname, be sure to use a unique name.
		This is a password-protected function. Unlock the protection level 1 to access it. See SYSTem. \n
			:param hostname: string
		"""
		param = Conversions.value_to_quoted_str(hostname)
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:COMMon:HOSTname {param}')

	def get_workgroup(self) -> str:
		"""SYSTem:COMMunicate:NETWork:[COMMon]:WORKgroup \n
		Sets an individual workgroup name for the instrument. \n
			:return: workgroup: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NETWork:COMMon:WORKgroup?')
		return trim_str_response(response)

	def set_workgroup(self, workgroup: str) -> None:
		"""SYSTem:COMMunicate:NETWork:[COMMon]:WORKgroup \n
		Sets an individual workgroup name for the instrument. \n
			:param workgroup: string
		"""
		param = Conversions.value_to_quoted_str(workgroup)
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:COMMon:WORKgroup {param}')
