from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get_predefined(self) -> List[str]:
		"""[SOURce<HW>]:BB:GNSS:VEHicle:CATalog:PREDefined \n
		Queries the names of the predefined vehicle description files in the system directory. Listed are files with the file
		extension *.xvd. \n
			:return: gnss_vehicle_cat_names: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:VEHicle:CATalog:PREDefined?')
		return Conversions.str_to_str_list(response)

	def get_user(self) -> List[str]:
		"""[SOURce<HW>]:BB:GNSS:VEHicle:CATalog:USER \n
		Queries the names of the user-defined vehicle description files in the default or in a specific directory. Listed are
		files with the file extension *.xvd. Refer to 'Accessing Files in the Default or Specified Directory' for general
		information on file handling in the default and in a specific directory. \n
			:return: gnss_vehicle_user_cat_names: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:VEHicle:CATalog:USER?')
		return Conversions.str_to_str_list(response)
