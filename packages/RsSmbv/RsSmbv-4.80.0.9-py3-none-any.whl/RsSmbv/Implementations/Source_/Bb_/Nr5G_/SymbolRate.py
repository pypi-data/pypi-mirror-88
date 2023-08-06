from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def get_variation(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:SRATe:VARiation \n
		No command help available \n
			:return: sym_rate_var: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SRATe:VARiation?')
		return Conversions.str_to_float(response)
