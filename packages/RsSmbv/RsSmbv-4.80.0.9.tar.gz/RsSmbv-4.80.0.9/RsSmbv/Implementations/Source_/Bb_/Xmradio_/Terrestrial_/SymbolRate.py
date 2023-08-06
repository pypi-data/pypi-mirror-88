from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def get_variation(self) -> int:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:SRATe:VARiation \n
		No command help available \n
			:return: variation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:TERRestrial:SRATe:VARiation?')
		return Conversions.str_to_int(response)
