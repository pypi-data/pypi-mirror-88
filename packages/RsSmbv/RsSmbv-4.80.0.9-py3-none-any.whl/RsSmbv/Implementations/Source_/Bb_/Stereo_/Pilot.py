from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pilot:
	"""Pilot commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pilot", core, parent)

	def get_phase(self) -> float:
		"""[SOURce<HW>]:BB:STEReo:PILot:PHASe \n
		No command help available \n
			:return: phase: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:PILot:PHASe?')
		return Conversions.str_to_float(response)

	def set_phase(self, phase: float) -> None:
		"""[SOURce<HW>]:BB:STEReo:PILot:PHASe \n
		No command help available \n
			:param phase: No help available
		"""
		param = Conversions.decimal_value_to_str(phase)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:PILot:PHASe {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:STEReo:PILot:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:PILot:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:STEReo:PILot:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:PILot:STATe {param}')

	def get_deviation(self) -> int:
		"""[SOURce<HW>]:BB:STEReo:PILot:[DEViation] \n
		No command help available \n
			:return: deviation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:PILot:DEViation?')
		return Conversions.str_to_int(response)

	def set_deviation(self, deviation: int) -> None:
		"""[SOURce<HW>]:BB:STEReo:PILot:[DEViation] \n
		No command help available \n
			:param deviation: No help available
		"""
		param = Conversions.decimal_value_to_str(deviation)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:PILot:DEViation {param}')
