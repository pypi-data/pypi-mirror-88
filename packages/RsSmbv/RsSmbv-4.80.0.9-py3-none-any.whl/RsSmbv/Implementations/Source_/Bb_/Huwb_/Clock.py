from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clock:
	"""Clock commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

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
	def sync(self):
		"""sync commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .Clock_.Sync import Sync
			self._sync = Sync(self._core, self._base)
		return self._sync

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.HrpUwbClocMode:
		"""[SOURce<HW>]:BB:HUWB:CLOCk:MODE \n
		Sets the type of externally supplied clock. \n
			:return: mode: SAMPle| MSAMple| CSAMple
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:CLOCk:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbClocMode)

	def set_mode(self, mode: enums.HrpUwbClocMode) -> None:
		"""[SOURce<HW>]:BB:HUWB:CLOCk:MODE \n
		Sets the type of externally supplied clock. \n
			:param mode: SAMPle| MSAMple| CSAMple
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.HrpUwbClocMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:CLOCk:MODE {param}')

	def get_multiplier(self) -> int:
		"""[SOURce<HW>]:BB:HUWB:CLOCk:MULTiplier \n
		No command help available \n
			:return: multiplier: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:CLOCk:MULTiplier?')
		return Conversions.str_to_int(response)

	def set_multiplier(self, multiplier: int) -> None:
		"""[SOURce<HW>]:BB:HUWB:CLOCk:MULTiplier \n
		No command help available \n
			:param multiplier: No help available
		"""
		param = Conversions.decimal_value_to_str(multiplier)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:CLOCk:MULTiplier {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ClockSourceB:
		"""[SOURce<HW>]:BB:HUWB:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference
			- ELCLock: External local clock
			- EXTernal = ELCLock: Setting only Provided for backward compatibility with other Rohde & Schwarz signal generators \n
			:return: source: INTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:CLOCk:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ClockSourceB)

	def set_source(self, source: enums.ClockSourceB) -> None:
		"""[SOURce<HW>]:BB:HUWB:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference
			- ELCLock: External local clock
			- EXTernal = ELCLock: Setting only Provided for backward compatibility with other Rohde & Schwarz signal generators \n
			:param source: INTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.ClockSourceB)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:CLOCk:SOURce {param}')
