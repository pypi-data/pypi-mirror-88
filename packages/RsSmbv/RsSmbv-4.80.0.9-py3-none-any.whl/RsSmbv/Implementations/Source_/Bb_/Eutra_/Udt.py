from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Udt:
	"""Udt commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("udt", core, parent)

	def get_cycle(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UDT:CYCLe \n
		No command help available \n
			:return: cycle: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UDT:CYCLe?')
		return Conversions.str_to_int(response)

	def set_cycle(self, cycle: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UDT:CYCLe \n
		No command help available \n
			:param cycle: No help available
		"""
		param = Conversions.decimal_value_to_str(cycle)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UDT:CYCLe {param}')

	def get_on_duration(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UDT:ONDuration \n
		No command help available \n
			:return: on_duration: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UDT:ONDuration?')
		return Conversions.str_to_int(response)

	def set_on_duration(self, on_duration: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UDT:ONDuration \n
		No command help available \n
			:param on_duration: No help available
		"""
		param = Conversions.decimal_value_to_str(on_duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UDT:ONDuration {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:UDT:STATe \n
		No command help available \n
			:return: test_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UDT:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, test_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UDT:STATe \n
		No command help available \n
			:param test_state: No help available
		"""
		param = Conversions.bool_to_str(test_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UDT:STATe {param}')
