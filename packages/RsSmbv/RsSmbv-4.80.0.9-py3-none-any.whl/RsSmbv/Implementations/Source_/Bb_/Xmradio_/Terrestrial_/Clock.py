from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clock:
	"""Clock commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clock", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClocModeB:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:CLOCk:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:TERRestrial:CLOCk:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClocModeB)

	def set_mode(self, mode: enums.ClocModeB) -> None:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:CLOCk:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClocModeB)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:TERRestrial:CLOCk:MODE {param}')

	def get_multiplier(self) -> int:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:CLOCk:MULTiplier \n
		No command help available \n
			:return: multiplier: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:TERRestrial:CLOCk:MULTiplier?')
		return Conversions.str_to_int(response)

	def set_multiplier(self, multiplier: int) -> None:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:CLOCk:MULTiplier \n
		No command help available \n
			:param multiplier: No help available
		"""
		param = Conversions.decimal_value_to_str(multiplier)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:TERRestrial:CLOCk:MULTiplier {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ClockSourceB:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:CLOCk:SOURce \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:TERRestrial:CLOCk:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ClockSourceB)

	def set_source(self, source: enums.ClockSourceB) -> None:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:CLOCk:SOURce \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.ClockSourceB)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:TERRestrial:CLOCk:SOURce {param}')
