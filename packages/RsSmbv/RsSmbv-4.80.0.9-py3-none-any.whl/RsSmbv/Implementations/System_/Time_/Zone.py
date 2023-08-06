from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zone:
	"""Zone commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zone", core, parent)

	def get_catalog(self) -> List[str]:
		"""SYSTem:TIME:ZONE:CATalog \n
		Querys the list of available timezones. \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:ZONE:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""SYSTem:TIME:ZONE \n
		Sets the timezone. You can query the list of the available timezones with method RsSmbv.System.Time.Zone.catalog. \n
			:return: time_zone: string
		"""
		response = self._core.io.query_str('SYSTem:TIME:ZONE?')
		return trim_str_response(response)

	def set_value(self, time_zone: str) -> None:
		"""SYSTem:TIME:ZONE \n
		Sets the timezone. You can query the list of the available timezones with method RsSmbv.System.Time.Zone.catalog. \n
			:param time_zone: string
		"""
		param = Conversions.value_to_quoted_str(time_zone)
		self._core.io.write(f'SYSTem:TIME:ZONE {param}')
