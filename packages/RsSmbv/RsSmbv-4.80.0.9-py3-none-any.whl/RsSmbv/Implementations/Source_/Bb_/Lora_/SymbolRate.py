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
		"""[SOURce<HW>]:BB:LORA:SRATe:VARiation \n
		Sets the sample rate of the signal. A variation of this parameter affects the ARB clock rate; all other signal parameters
		remain unchanged. When changing values of the affecting parameters, the sample rate is reset. \n
			:return: variation: float Range: 4E2 to 20E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:SRATe:VARiation?')
		return Conversions.str_to_float(response)

	def set_variation(self, variation: float) -> None:
		"""[SOURce<HW>]:BB:LORA:SRATe:VARiation \n
		Sets the sample rate of the signal. A variation of this parameter affects the ARB clock rate; all other signal parameters
		remain unchanged. When changing values of the affecting parameters, the sample rate is reset. \n
			:param variation: float Range: 4E2 to 20E6
		"""
		param = Conversions.decimal_value_to_str(variation)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:SRATe:VARiation {param}')
