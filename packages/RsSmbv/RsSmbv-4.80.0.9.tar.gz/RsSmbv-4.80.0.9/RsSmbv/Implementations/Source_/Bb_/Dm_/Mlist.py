from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mlist:
	"""Mlist commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mlist", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:DM:MLISt:CATalog \n
		Reads out the list files present in the default directory (see method RsSmbv.MassMemory.currentDirectory) .
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam
		Refer to 'Accessing Files in the Default or in a Specified Directory' for general information on file handling in the
		default and a specific directory. \n
			:return: catalog: 'filename1,filename2,...' Returns a string of file names separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:MLISt:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:MLISt:DELete \n
		Deletes the specified list from the default directory (see method RsSmbv.MassMemory.currentDirectory) or from the
		directory specified with the absolute file path. Refer to 'Accessing Files in the Default or in a Specified Directory'
		for general information on file handling in the default and a specific directory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User standard / ...:ULISt... / *.dm_stu
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:MLISt:DELete {param}')

	def get_free(self) -> int:
		"""[SOURce<HW>]:BB:DM:MLISt:FREE \n
		Queries the list free memory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:return: free: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:MLISt:FREE?')
		return Conversions.str_to_int(response)

	def get_points(self) -> int:
		"""[SOURce<HW>]:BB:DM:MLISt:POINts \n
		Queries the user modulation mapping/user filter list length. \n
			:return: points: integer Range: max
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:MLISt:POINts?')
		return Conversions.str_to_int(response)

	def get_select(self) -> str:
		"""[SOURce<HW>]:BB:DM:MLISt:SELect \n
		Selects the specified list file from the default directory (see method RsSmbv.MassMemory.currentDirectory) or in the
		directory specified with the absolute file path. If a list with the specified name does not yet exist, it is created. The
		file extension can be omitted. Refer to 'Accessing Files in the Default or in a Specified Directory' for general
		information on file handling in the default and a specific directory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User standard / ...:ULISt... / *.dm_stu
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:MLISt:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:MLISt:SELect \n
		Selects the specified list file from the default directory (see method RsSmbv.MassMemory.currentDirectory) or in the
		directory specified with the absolute file path. If a list with the specified name does not yet exist, it is created. The
		file extension can be omitted. Refer to 'Accessing Files in the Default or in a Specified Directory' for general
		information on file handling in the default and a specific directory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User standard / ...:ULISt... / *.dm_stu
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:param filename: list name
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:MLISt:SELect {param}')
