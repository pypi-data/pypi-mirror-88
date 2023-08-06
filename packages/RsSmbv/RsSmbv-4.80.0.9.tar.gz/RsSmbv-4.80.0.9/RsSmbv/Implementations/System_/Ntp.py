from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ntp:
	"""Ntp commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ntp", core, parent)

	def get_hostname(self) -> str:
		"""SYSTem:NTP:HOSTname \n
		Sets the address of the NTP server. You can enter the IP address, or the hostname of the time server, or even set up an
		own vendor zone. See the Internet for more information on NTP. \n
			:return: ntp_name: string
		"""
		response = self._core.io.query_str('SYSTem:NTP:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, ntp_name: str) -> None:
		"""SYSTem:NTP:HOSTname \n
		Sets the address of the NTP server. You can enter the IP address, or the hostname of the time server, or even set up an
		own vendor zone. See the Internet for more information on NTP. \n
			:param ntp_name: string
		"""
		param = Conversions.value_to_quoted_str(ntp_name)
		self._core.io.write(f'SYSTem:NTP:HOSTname {param}')

	def get_state(self) -> bool:
		"""SYSTem:NTP:STATe \n
		Activates clock synchronization via NTP. \n
			:return: use_ntp_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SYSTem:NTP:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, use_ntp_state: bool) -> None:
		"""SYSTem:NTP:STATe \n
		Activates clock synchronization via NTP. \n
			:param use_ntp_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(use_ntp_state)
		self._core.io.write(f'SYSTem:NTP:STATe {param}')
