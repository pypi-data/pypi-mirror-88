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
		"""[SOURce<HW>]:BB:OFDM:SRATe:VARiation \n
		Sets the symbol rate variation of the signal. \n
			:return: sym_rate_var: float Range: 400 to 4E7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:SRATe:VARiation?')
		return Conversions.str_to_float(response)

	def set_variation(self, sym_rate_var: float) -> None:
		"""[SOURce<HW>]:BB:OFDM:SRATe:VARiation \n
		Sets the symbol rate variation of the signal. \n
			:param sym_rate_var: float Range: 400 to 4E7
		"""
		param = Conversions.decimal_value_to_str(sym_rate_var)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:SRATe:VARiation {param}')
