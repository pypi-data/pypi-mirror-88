from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 6 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	def clone(self) -> 'Setting':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Setting(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def tmod(self):
		"""tmod commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tmod'):
			from .Setting_.Tmod import Tmod
			self._tmod = Tmod(self._core, self._base)
		return self._tmod

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:CATalog \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.lte.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: catalog: filename1,filename2,... Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def set_del_py(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:DEL \n
		Deletes the selected file from the default or the specified directory. Deleted are files with extension *.lte. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:param filename: string Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SETTing:DEL {param}')

	def get_load(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.lte.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: string Filename or complete file path; file extension can be omitted
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SETTing:LOAD?')
		return trim_str_response(response)

	def set_load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.lte.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SETTing:LOAD {param}')

	def get_store(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:STORe \n
		Stores the current settings into the selected file; the file extension (*.lte) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: string Filename or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SETTing:STORe?')
		return trim_str_response(response)

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:STORe \n
		Stores the current settings into the selected file; the file extension (*.lte) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SETTing:STORe {param}')
