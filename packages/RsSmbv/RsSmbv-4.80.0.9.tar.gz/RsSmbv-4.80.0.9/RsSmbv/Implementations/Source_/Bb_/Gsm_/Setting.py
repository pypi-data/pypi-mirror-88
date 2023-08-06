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

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:GSM:SETTing:CATalog \n
		This command reads out the files with GSM settings in the default directory. The default directory is set using command
		method RsSmbv.MassMemory.currentDirectory. Only files with the file extension *.gsm are listed. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GSM:SETTing:DELete \n
		This command deletes the selected file with GSM settings. The directory is set using command method RsSmbv.MassMemory.
		currentDirectory. A path can also be specified, in which case the files in the specified directory are read. The file
		extension can be omitted. Only files with the file extension *.gsm are deleted. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GSM:SETTing:LOAD \n
		This command loads the selected file with GSM settings. The directory is set using command method RsSmbv.MassMemory.
		currentDirectory. A path can also be specified, in which case the files in the specified directory are read. The file
		extension can be omitted. Only files with the file extension *.gsm are loaded. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GSM:SETTing:STORe \n
		This command stores the current GSM settings into the selected file. The directory is set using command method RsSmbv.
		MassMemory.currentDirectory. A path can also be specified, in which case the files in the specified directory are read.
		Only enter the file name. GSM settings are stored as files with the specific file extensions *.gsm. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:SETTing:STORe {param}')
