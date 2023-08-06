from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdw:
	"""Tdw commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdw", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:TDW:STATe \n
		Activates/deactivates the time domain windowing. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TDW:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TDW:STATe \n
		Activates/deactivates the time domain windowing. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TDW:STATe {param}')

	def get_tr_time(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:TDW:TRTime \n
		Sets the transition time when time domain windowing is active. \n
			:return: transition_time: float Range: 0 to 1E-5, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TDW:TRTime?')
		return Conversions.str_to_float(response)

	def set_tr_time(self, transition_time: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TDW:TRTime \n
		Sets the transition time when time domain windowing is active. \n
			:param transition_time: float Range: 0 to 1E-5, Unit: s
		"""
		param = Conversions.decimal_value_to_str(transition_time)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TDW:TRTime {param}')
