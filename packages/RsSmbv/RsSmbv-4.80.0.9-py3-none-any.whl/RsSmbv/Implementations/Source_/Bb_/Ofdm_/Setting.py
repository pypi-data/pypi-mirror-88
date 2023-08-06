from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:OFDM:SETTing:CATalog \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.c5g.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: c_5_gcat_name: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_del_py(self) -> str:
		"""[SOURce<HW>]:BB:OFDM:SETTing:DEL \n
		Deletes the selected file from the default or specified directory. Deleted are files with the file extension *.c5g. Refer
		to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in
		a specific directory. \n
			:return: filename: string file name or complete file path; file extension can be omitted
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:SETTing:DEL?')
		return trim_str_response(response)

	def set_del_py(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:OFDM:SETTing:DEL \n
		Deletes the selected file from the default or specified directory. Deleted are files with the file extension *.c5g. Refer
		to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in
		a specific directory. \n
			:param filename: string file name or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:SETTing:DEL {param}')

	def get_load(self) -> str:
		"""[SOURce<HW>]:BB:OFDM:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.c5g.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: string file name or complete file path; file extension can be omitted
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:SETTing:LOAD?')
		return trim_str_response(response)

	def set_load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:OFDM:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.c5g.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string file name or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:SETTing:LOAD {param}')

	def get_store(self) -> str:
		"""[SOURce<HW>]:BB:OFDM:SETTing:STORe \n
		Stores the current settings into the selected file; the file extension (*.c5g) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filename: string file name or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:SETTing:STORe?')
		return trim_str_response(response)

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:OFDM:SETTing:STORe \n
		Stores the current settings into the selected file; the file extension (*.c5g) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string file name or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:SETTing:STORe {param}')
