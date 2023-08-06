from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ulist:
	"""Ulist commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ulist", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:DM:STANdard:ULISt:CATalog \n
		Queries the files with digital modulation respectively user standard settings in the default directory. Listed are files
		with the file extension *.dm and *.dm_stu. Refer to 'Accessing Files in the Default or in a Specified Directory' for
		general information on file handling in the default and a specific directory. \n
			:return: catalog: 'filename1,filename2,...' Returns a string of file names separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:STANdard:ULISt:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:STANdard:ULISt:DELete \n
		Deletes the selected file from the default or specified directory. Deleted are files with the file extension *.
		dm respectively *.dm_stu. Refer to 'Accessing Files in the Default or in a Specified Directory' for general information
		on file handling in the default and a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:STANdard:ULISt:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:STANdard:ULISt:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.dm respectively *.
		dm_stu. Refer to 'Accessing Files in the Default or in a Specified Directory' for general information on file handling in
		the default and a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:STANdard:ULISt:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:STANdard:ULISt:STORe \n
		Stores the current settings into the selected file; the file extension (*.dm respectively *.
		dm_stu) is assigned automatically. Refer to 'Accessing Files in the Default or in a Specified Directory' for general
		information on file handling in the default and a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:STANdard:ULISt:STORe {param}')
