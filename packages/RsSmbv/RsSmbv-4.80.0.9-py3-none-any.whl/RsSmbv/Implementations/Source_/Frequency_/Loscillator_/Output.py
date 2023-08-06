from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:FREQuency:LOSCillator:OUTPut:FREQuency \n
		Queries the current frequency of the local oscillator at the [LO Out] connector. \n
			:return: frequency: float Range: 100E3 to 20E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:LOSCillator:OUTPut:FREQuency?')
		return Conversions.str_to_float(response)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:FREQuency:LOSCillator:OUTPut:STATe \n
		Activates the LO output. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:LOSCillator:OUTPut:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:FREQuency:LOSCillator:OUTPut:STATe \n
		Activates the LO output. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:LOSCillator:OUTPut:STATe {param}')
