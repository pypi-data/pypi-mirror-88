from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Predefined:
	"""Predefined commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("predefined", core, parent)

	def get_catalog(self) -> List[str]:
		"""SYSTem:DEXChange:TEMPlate:PREDefined:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SYSTem:DEXChange:TEMPlate:PREDefined:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_select(self) -> str:
		"""SYSTem:DEXChange:TEMPlate:PREDefined:SELect \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SYSTem:DEXChange:TEMPlate:PREDefined:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SYSTem:DEXChange:TEMPlate:PREDefined:SELect \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SYSTem:DEXChange:TEMPlate:PREDefined:SELect {param}')
