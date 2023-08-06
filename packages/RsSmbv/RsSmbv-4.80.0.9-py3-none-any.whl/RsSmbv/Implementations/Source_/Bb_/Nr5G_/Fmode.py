from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fmode:
	"""Fmode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fmode", core, parent)

	def get_usr_file(self) -> str:
		"""[SOURce<HW>]:BB:NR5G:FMODe:USRFile \n
		Loads the file from the default or the specified directory. Loaded are files with extension *.vaf or *.dat.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: filter_file_name: string Complete file path incl. filename and extension
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:FMODe:USRFile?')
		return trim_str_response(response)

	def set_usr_file(self, filter_file_name: str) -> None:
		"""[SOURce<HW>]:BB:NR5G:FMODe:USRFile \n
		Loads the file from the default or the specified directory. Loaded are files with extension *.vaf or *.dat.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filter_file_name: string Complete file path incl. filename and extension
		"""
		param = Conversions.value_to_quoted_str(filter_file_name)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:FMODe:USRFile {param}')
