from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clock:
	"""Clock commands group definition. 6 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clock", core, parent)

	def clone(self) -> 'Clock':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Clock(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def synchronization(self):
		"""synchronization commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_synchronization'):
			from .Clock_.Synchronization import Synchronization
			self._synchronization = Synchronization(self._core, self._base)
		return self._synchronization

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClocModeB:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClocModeB)

	def set_mode(self, mode: enums.ClocModeB) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClocModeB)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk:MODE {param}')

	def get_multiplier(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk:MULTiplier \n
		No command help available \n
			:return: multiplier: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk:MULTiplier?')
		return Conversions.str_to_int(response)

	def set_multiplier(self, multiplier: int) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk:MULTiplier \n
		No command help available \n
			:param multiplier: No help available
		"""
		param = Conversions.decimal_value_to_str(multiplier)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk:MULTiplier {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ClockSourceA:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference \n
			:return: source: INTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ClockSourceA)

	def set_source(self, source: enums.ClockSourceA) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference \n
			:param source: INTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.ClockSourceA)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk:SOURce {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk \n
		Sets the clock frequency. If you load a waveform, the clock rate is determined as defined with the waveform tag {CLOCK:​
		frequency}. This command subsequently changes the clock rate; see data sheet for value range. \n
			:return: clock: float Range: depends on the installed options , Unit: Hz E.g. 400 Hz to 600 MHz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk?')
		return Conversions.str_to_float(response)

	def set_value(self, clock: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk \n
		Sets the clock frequency. If you load a waveform, the clock rate is determined as defined with the waveform tag {CLOCK:​
		frequency}. This command subsequently changes the clock rate; see data sheet for value range. \n
			:param clock: float Range: depends on the installed options , Unit: Hz E.g. 400 Hz to 600 MHz
		"""
		param = Conversions.decimal_value_to_str(clock)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk {param}')
