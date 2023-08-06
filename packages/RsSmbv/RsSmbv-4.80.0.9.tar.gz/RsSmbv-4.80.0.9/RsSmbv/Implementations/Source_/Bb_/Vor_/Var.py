from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Var:
	"""Var commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("var", core, parent)

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:VAR:FREQuency \n
		Sets the frequency of the variable and the reference signal. As the two signals must have the same frequency, the setting
		is valid for both signals. \n
			:return: frequency: float Range: 10 to 60
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:VAR:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:VAR:FREQuency \n
		Sets the frequency of the variable and the reference signal. As the two signals must have the same frequency, the setting
		is valid for both signals. \n
			:param frequency: float Range: 10 to 60
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:VAR:FREQuency {param}')

	def get_depth(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:VAR:[DEPTh] \n
		Sets the AM modulation depth of the 30 Hz variable signal. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:VAR:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:VAR:[DEPTh] \n
		Sets the AM modulation depth of the 30 Hz variable signal. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:VAR:DEPTh {param}')
