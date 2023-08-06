from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:SETTing:CATalog \n
		Queries the files with I/Q output settings in the default directory. Listed are files with the file extension *.iqout. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:SETTing:DELete \n
		Deletes the selected file from the default or specified directory. Deleted are files with the file extension *.iqout. \n
			:param filename: 'filename' Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.iqout. \n
			:param filename: 'filename' Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:SETTing:STORe \n
		Stores the current settings into the selected file; the file extension (*.iqout) is assigned automatically. \n
			:param filename: 'filename' Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:SETTing:STORe {param}')
