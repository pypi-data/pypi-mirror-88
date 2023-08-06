from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DME:SETTing:DELete \n
		Deletes the selected file from the default or the specified directory. Deleted are files with extension *.vor/*.ils/*.dme.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DME:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.vor/*.ils/*.dme.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DME:SETTing:STORe \n
		Saves the current settings into the selected file; the file extension (*.vor/*.ils/*.dme) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SETTing:STORe {param}')

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:[BB]:DME:SETTing:CATalog \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.vor/*.ils/*.dme.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: avionic_dme_cat_names: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)
