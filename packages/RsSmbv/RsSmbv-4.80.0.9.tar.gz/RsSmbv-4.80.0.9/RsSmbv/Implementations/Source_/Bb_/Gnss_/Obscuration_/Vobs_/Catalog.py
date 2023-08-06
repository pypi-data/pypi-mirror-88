from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get_predefined(self) -> List[str]:
		"""[SOURce<HW>]:BB:GNSS:OBSCuration:VOBS:CATalog:PREDefined \n
		Queries the names of predefined files in the system directory.
			INTRO_CMD_HELP: Listed are only the following file types: \n
			- Obstacles description files (*.rs_obst)
			- Roadside buildings description files (*.rs_buil)
			- Land mobile multipath (LMM) files (*.lmm)  \n
			:return: gnss_obsc_vert_obst_cat_names: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:OBSCuration:VOBS:CATalog:PREDefined?')
		return Conversions.str_to_str_list(response)

	def get_user(self) -> List[str]:
		"""[SOURce<HW>]:BB:GNSS:OBSCuration:VOBS:CATalog:USER \n
		Queries the names of the user-defined files in the default directory. The default directory is set using command method
		RsSmbv.MassMemory.currentDirectory.
			INTRO_CMD_HELP: Listed are the following file types: \n
			- Obstacles description files (*.rs_obst)
			- Roadside buildings description files (*.rs_buil)
			- Land mobile multipath (LMM) files (*.lmm)  \n
			:return: gnss_obsc_vert_obst_user_cat_names: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:OBSCuration:VOBS:CATalog:USER?')
		return Conversions.str_to_str_list(response)
