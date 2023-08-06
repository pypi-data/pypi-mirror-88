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
		"""[SOURce<HW>]:BB:EUTRa:SRATe:VARiation \n
		Sets the output sample rate. A variation of this parameter affects the ARB clock rate; all other signal parameters remain
		unchanged. The current value of this parameter depends on the current physical settings, like the channel bandwidth. \n
			:return: variation: float Range: 400 to 4E7, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SRATe:VARiation?')
		return Conversions.str_to_float(response)

	def set_variation(self, variation: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:SRATe:VARiation \n
		Sets the output sample rate. A variation of this parameter affects the ARB clock rate; all other signal parameters remain
		unchanged. The current value of this parameter depends on the current physical settings, like the channel bandwidth. \n
			:param variation: float Range: 400 to 4E7, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(variation)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SRATe:VARiation {param}')
