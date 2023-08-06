from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get(self, name: str) -> List[str]:
		"""SYSTem:PROFiling:TPOint:CATalog \n
		No command help available \n
			:param name: No help available
			:return: value: No help available"""
		param = Conversions.value_to_quoted_str(name)
		response = self._core.io.query_str(f'SYSTem:PROFiling:TPOint:CATalog? {param}')
		return Conversions.str_to_str_list(response)
