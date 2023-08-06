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
		"""[SOURce<HW>]:BB:WLNN:SETTing:CATalog \n
		Reads out the files with IEEE 802.11a/b/g/n/ac settings in the default directory. The default directory is set using
		command method RsSmbv.MassMemory.currentDirectory. Only files with the file extension *.wlann will be listed. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:WLNN:SETTing:DELete \n
		Deletes the selected file with IIEEE 802.11a/b/g/n/ac settings. The directory is set using command method RsSmbv.
		MassMemory.currentDirectory. A path can also be specified, in which case the files in the specified directory are read.
		The file extension may be omitted. Only files with the file extension *.wlann are listed and can be deleted. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:WLNN:SETTing:LOAD \n
		Loads the selected file with IEEE 802.11 WLAN settings. The directory is set using command method RsSmbv.MassMemory.
		currentDirectory. A path can also be specified, in which case the files in the specified directory are read. The file
		extension may be omitted. Only files with the file extension *.wlann will be loaded. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:WLNN:SETTing:STORe \n
		Stores the current IEEE 802.11a/b/g/n/ac settings into the selected file. The directory is set using command method
		RsSmbv.MassMemory.currentDirectory. A path can also be specified, in which case the files in the specified directory are
		read. Only the file name has to be entered. IEEE 802.11a/b/g/n/ac settings are stored as files with the specific file
		extensions *.wlann. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:SETTing:STORe {param}')
