from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:USER:CATalog \n
		The command queries existing files with stored user channel codings. The files are stored with the fixed file extensions
		*.3g_ccod_ul in a directory of the user's choice. The directory applicable to the commands is defined with the command
		method RsSmbv.MassMemory.currentDirectory. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:USER:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:USER:DELete \n
		The command deletes the specified files with stored user channel codings. The files are stored with the fixed file
		extensions *.3g_ccod_ul in a directory of the user's choice. The directory applicable to the commands is defined with the
		command method RsSmbv.MassMemory.currentDirectory. To access the files in this directory, you only have to give the file
		name, without the path and the file extension. The command triggers an event and therefore has no query form and no *RST
		value. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:USER:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:USER:LOAD \n
		The command loads the specified files with stored user channel codings. The files are stored with the fixed file
		extensions *.3g_ccod_ul in a directory of the user's choice. The directory applicable to the commands is defined with the
		command method RsSmbv.MassMemory.currentDirectory. To access the files in this directory, you only have to give the file
		name, without the path and the file extension. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:USER:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:USER:STORe \n
		The command saves the current settings for channel coding as user channel coding in the specified file. The files are
		stored with the fixed file extensions *.3g_ccod_ul in a directory of the user's choice. The directory in which the file
		is stored is defined with the command method RsSmbv.MassMemory.currentDirectory. To store the files in this directory,
		you only have to give the file name, without the path and the file extension. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:USER:STORe {param}')
