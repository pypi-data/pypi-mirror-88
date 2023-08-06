from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fsk:
	"""Fsk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fsk", core, parent)

	def get_deviation(self) -> float:
		"""[SOURce<HW>]:BB:GSM:FSK:DEViation \n
		Sets the modulation deviation when BB:GSM:FORMat FSK2 is selected. The range of values depends on the symbol rate (method
		RsSmbv.Source.Bb.Gsm.SymbolRate.value) . The maximum deviation is 10 MHz. \n
			:return: deviation: float Range: 0.1xf(symb) to 1.5xf(symb) ;(10MHz) , Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:FSK:DEViation?')
		return Conversions.str_to_float(response)

	def set_deviation(self, deviation: float) -> None:
		"""[SOURce<HW>]:BB:GSM:FSK:DEViation \n
		Sets the modulation deviation when BB:GSM:FORMat FSK2 is selected. The range of values depends on the symbol rate (method
		RsSmbv.Source.Bb.Gsm.SymbolRate.value) . The maximum deviation is 10 MHz. \n
			:param deviation: float Range: 0.1xf(symb) to 1.5xf(symb) ;(10MHz) , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(deviation)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FSK:DEViation {param}')
