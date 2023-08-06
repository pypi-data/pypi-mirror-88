from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Version:
	"""Version commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("version", core, parent)

	def get_catalog(self) -> List[str]:
		"""SYSTem:SPECification:VERSion:CATalog \n
		Queries all data sheet versions stored in the instrument. \n
			:return: vers_catalog: string
		"""
		response = self._core.io.query_str('SYSTem:SPECification:VERSion:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_factory(self) -> str:
		"""SYSTem:SPECification:VERSion:FACTory \n
		Queries the data sheet version of the factory setting. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SYSTem:SPECification:VERSion:FACTory?')
		return trim_str_response(response)

	def get_sfactory(self) -> str:
		"""SYSTem:SPECification:VERSion:SFACtory \n
		No command help available \n
			:return: ds_fact_version: No help available
		"""
		response = self._core.io.query_str('SYSTem:SPECification:VERSion:SFACtory?')
		return trim_str_response(response)

	def set_sfactory(self, ds_fact_version: str) -> None:
		"""SYSTem:SPECification:VERSion:SFACtory \n
		No command help available \n
			:param ds_fact_version: No help available
		"""
		param = Conversions.value_to_quoted_str(ds_fact_version)
		self._core.io.write(f'SYSTem:SPECification:VERSion:SFACtory {param}')

	def get_value(self) -> str:
		"""SYSTem:SPECification:VERSion \n
		Selects a data sheet version from the data sheets saved on the instrument. Further queries regarding the data sheet
		parameters (<Id>) and their values refer to the selected data sheet. To query the list of data sheet versions, use the
		command method RsSmbv.System.Specification.Version.catalog. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SYSTem:SPECification:VERSion?')
		return trim_str_response(response)

	def set_value(self, version: str) -> None:
		"""SYSTem:SPECification:VERSion \n
		Selects a data sheet version from the data sheets saved on the instrument. Further queries regarding the data sheet
		parameters (<Id>) and their values refer to the selected data sheet. To query the list of data sheet versions, use the
		command method RsSmbv.System.Specification.Version.catalog. \n
			:param version: string
		"""
		param = Conversions.value_to_quoted_str(version)
		self._core.io.write(f'SYSTem:SPECification:VERSion {param}')
