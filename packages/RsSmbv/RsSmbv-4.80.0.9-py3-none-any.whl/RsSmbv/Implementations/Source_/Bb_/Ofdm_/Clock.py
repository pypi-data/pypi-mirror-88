from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clock:
	"""Clock commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clock", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.EuTraClockMode:
		"""[SOURce<HW>]:BB:OFDM:CLOCk:MODE \n
		No command help available \n
			:return: clock_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:CLOCk:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EuTraClockMode)

	def set_mode(self, clock_mode: enums.EuTraClockMode) -> None:
		"""[SOURce<HW>]:BB:OFDM:CLOCk:MODE \n
		No command help available \n
			:param clock_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(clock_mode, enums.EuTraClockMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:CLOCk:MODE {param}')

	def get_multiplier(self) -> int:
		"""[SOURce<HW>]:BB:OFDM:CLOCk:MULTiplier \n
		No command help available \n
			:return: clock_samp_mult: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:CLOCk:MULTiplier?')
		return Conversions.str_to_int(response)

	def set_multiplier(self, clock_samp_mult: int) -> None:
		"""[SOURce<HW>]:BB:OFDM:CLOCk:MULTiplier \n
		No command help available \n
			:param clock_samp_mult: No help available
		"""
		param = Conversions.decimal_value_to_str(clock_samp_mult)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:CLOCk:MULTiplier {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ClockSourceA:
		"""[SOURce<HW>]:BB:OFDM:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference \n
			:return: clock_sour: INTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:CLOCk:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ClockSourceA)

	def set_source(self, clock_sour: enums.ClockSourceA) -> None:
		"""[SOURce<HW>]:BB:OFDM:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference \n
			:param clock_sour: INTernal
		"""
		param = Conversions.enum_scalar_to_str(clock_sour, enums.ClockSourceA)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:CLOCk:SOURce {param}')
