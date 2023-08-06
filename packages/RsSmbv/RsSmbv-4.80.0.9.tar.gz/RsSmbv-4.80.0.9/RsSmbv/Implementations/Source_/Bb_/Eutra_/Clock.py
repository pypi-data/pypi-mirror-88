from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clock:
	"""Clock commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clock", core, parent)

	def get_custom(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:CLOCk:CUSTom \n
		No command help available \n
			:return: custom: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:CLOCk:CUSTom?')
		return Conversions.str_to_int(response)

	def set_custom(self, custom: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:CLOCk:CUSTom \n
		No command help available \n
			:param custom: No help available
		"""
		param = Conversions.decimal_value_to_str(custom)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:CLOCk:CUSTom {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.EuTraClockMode:
		"""[SOURce<HW>]:BB:EUTRa:CLOCk:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:CLOCk:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EuTraClockMode)

	def set_mode(self, mode: enums.EuTraClockMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:CLOCk:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.EuTraClockMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:CLOCk:MODE {param}')

	def get_multiplier(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:CLOCk:MULTiplier \n
		No command help available \n
			:return: multiplier: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:CLOCk:MULTiplier?')
		return Conversions.str_to_int(response)

	def set_multiplier(self, multiplier: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:CLOCk:MULTiplier \n
		No command help available \n
			:param multiplier: No help available
		"""
		param = Conversions.decimal_value_to_str(multiplier)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:CLOCk:MULTiplier {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ClockSourceA:
		"""[SOURce<HW>]:BB:EUTRa:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference \n
			:return: source: INTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:CLOCk:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ClockSourceA)

	def set_source(self, source: enums.ClockSourceA) -> None:
		"""[SOURce<HW>]:BB:EUTRa:CLOCk:SOURce \n
			INTRO_CMD_HELP: Selects the clock source: \n
			- INTernal: Internal clock reference \n
			:param source: INTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.ClockSourceA)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:CLOCk:SOURce {param}')
