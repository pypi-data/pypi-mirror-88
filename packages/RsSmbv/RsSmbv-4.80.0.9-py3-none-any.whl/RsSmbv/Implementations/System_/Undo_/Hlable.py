from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hlable:
	"""Hlable commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hlable", core, parent)

	def get_catalog(self) -> List[str]:
		"""SYSTem:UNDO:HLABle:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SYSTem:UNDO:HLABle:CATalog?')
		return Conversions.str_to_str_list(response)

	def set_select(self, label: str) -> None:
		"""SYSTem:UNDO:HLABle:SELect \n
		No command help available \n
			:param label: No help available
		"""
		param = Conversions.value_to_quoted_str(label)
		self._core.io.write(f'SYSTem:UNDO:HLABle:SELect {param}')
