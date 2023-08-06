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
		"""[SOURce<HW>]:BB:NFC:SETTing:CATalog \n
		Catalog settings file name. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:NFC:SETTing:DELete \n
		Deletes the NFC settings file with the filename given in the parameter. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:NFC:SETTing:LOAD \n
		Loads the NFC setting file with the name given in the parameter. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:NFC:SETTing:STORe \n
		Stores current NFC settings in a file with the name given in the parameter. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:SETTing:STORe {param}')
