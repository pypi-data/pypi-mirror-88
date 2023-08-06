from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unit:
	"""Unit commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unit", core, parent)

	# noinspection PyTypeChecker
	def get_time(self) -> enums.UnitTimeSecMs:
		"""[SOURce<HW>]:BB:BTOoth:UNIT:TIME \n
		Sets the time unit for remote control commands. \n
			:return: time: S| MS
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:UNIT:TIME?')
		return Conversions.str_to_scalar_enum(response, enums.UnitTimeSecMs)

	def set_time(self, time: enums.UnitTimeSecMs) -> None:
		"""[SOURce<HW>]:BB:BTOoth:UNIT:TIME \n
		Sets the time unit for remote control commands. \n
			:param time: S| MS
		"""
		param = Conversions.enum_scalar_to_str(time, enums.UnitTimeSecMs)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:UNIT:TIME {param}')
