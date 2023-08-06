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
		"""[SOURce<HW>]:BB:GNSS:SETTing:CATalog:PREDefined \n
		Queries the files with predefined settings. \n
			:return: gnss_gnss_predefined_cat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SETTing:CATalog:PREDefined?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> List[str]:
		"""[SOURce<HW>]:BB:GNSS:SETTing:CATalog \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.gnss.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: gnss_gnss_sav_rcl_cat_names: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)
