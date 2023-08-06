from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dlist:
	"""Dlist commands group definition. 9 total commands, 1 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dlist", core, parent)

	def clone(self) -> 'Dlist':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dlist(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Dlist_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:DM:DLISt:CATalog \n
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
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:DLISt:CATalog?')
		return Conversions.str_to_str_list(response)

	def copy(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:DLISt:COPY \n
		Copies the selected data list (*.dm_iqd) / control list (*.dm_iqc) as a new list with name specified by <Filename>. If a
		list with the specified name exists, it is overwritten. If it does not yet exist, it is created. The source file has to
		be available in the default directory (see method RsSmbv.MassMemory.currentDirectory) . Refer to 'Accessing Files in the
		Default or in a Specified Directory' for general information on file handling in the default and a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:DLISt:COPY {param}')

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:DLISt:DELete \n
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
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:DLISt:DELete {param}')

	def get_free(self) -> int:
		"""[SOURce<HW>]:BB:DM:DLISt:FREE \n
		Queries the list free memory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:return: free: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:DLISt:FREE?')
		return Conversions.str_to_int(response)

	def get_points(self) -> int:
		"""[SOURce<HW>]:BB:DM:DLISt:POINts \n
		Defines the number of bits in the selected data list to be utilized. When a list is being filled with block data, this
		data is only ever sent in multiples of 8 bits. However the exact number of bits to be exploited can be set to a different
		figure. The superfluous bits in the list are then ignored. \n
			:return: points: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:DLISt:POINts?')
		return Conversions.str_to_int(response)

	def set_points(self, points: int) -> None:
		"""[SOURce<HW>]:BB:DM:DLISt:POINts \n
		Defines the number of bits in the selected data list to be utilized. When a list is being filled with block data, this
		data is only ever sent in multiples of 8 bits. However the exact number of bits to be exploited can be set to a different
		figure. The superfluous bits in the list are then ignored. \n
			:param points: integer Range: 0 to INT_MAX
		"""
		param = Conversions.decimal_value_to_str(points)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:DLISt:POINts {param}')

	def get_select(self) -> str:
		"""[SOURce<HW>]:BB:DM:DLISt:SELect \n
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
			:return: select: list name
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:DLISt:SELect?')
		return trim_str_response(response)

	def set_select(self, select: str) -> None:
		"""[SOURce<HW>]:BB:DM:DLISt:SELect \n
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
			:param select: list name
		"""
		param = Conversions.value_to_quoted_str(select)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:DLISt:SELect {param}')

	def get_tag(self) -> str:
		"""[SOURce<HW>]:BB:DM:DLISt:TAG \n
		Queries the content of the specified tag in the selected file. \n
			:return: tag: control list,tag name Refer to 'Tags for Waveforms, Data and Control Lists' for description of the available tag formats.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:DLISt:TAG?')
		return trim_str_response(response)
