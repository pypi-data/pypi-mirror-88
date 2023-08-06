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
	def get_mode(self) -> enums.Nr5GclocMode:
		"""[SOURce<HW>]:BB:NR5G:CLOCk:MODE \n
		No command help available \n
			:return: clock_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:CLOCk:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5GclocMode)

	def set_mode(self, clock_mode: enums.Nr5GclocMode) -> None:
		"""[SOURce<HW>]:BB:NR5G:CLOCk:MODE \n
		No command help available \n
			:param clock_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(clock_mode, enums.Nr5GclocMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:CLOCk:MODE {param}')

	def get_multiplier(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:CLOCk:MULTiplier \n
		No command help available \n
			:return: clock_samp_mult: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:CLOCk:MULTiplier?')
		return Conversions.str_to_int(response)

	def set_multiplier(self, clock_samp_mult: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:CLOCk:MULTiplier \n
		No command help available \n
			:param clock_samp_mult: No help available
		"""
		param = Conversions.decimal_value_to_str(clock_samp_mult)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:CLOCk:MULTiplier {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ClockSourceC:
		"""[SOURce<HW>]:BB:NR5G:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference \n
			:return: clock_sour: INTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:CLOCk:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ClockSourceC)

	def set_source(self, clock_sour: enums.ClockSourceC) -> None:
		"""[SOURce<HW>]:BB:NR5G:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference \n
			:param clock_sour: INTernal
		"""
		param = Conversions.enum_scalar_to_str(clock_sour, enums.ClockSourceC)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:CLOCk:SOURce {param}')
