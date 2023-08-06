from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_reference(self) -> float:
		"""[SOURce<HW>]:BB:GNSS:POWer:REFerence \n
		Sets the power level that is used as a reference for the calculation of the power level of the satellites. \n
			:return: reference_power: float Range: -145 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:POWer:REFerence?')
		return Conversions.str_to_float(response)

	def set_reference(self, reference_power: float) -> None:
		"""[SOURce<HW>]:BB:GNSS:POWer:REFerence \n
		Sets the power level that is used as a reference for the calculation of the power level of the satellites. \n
			:param reference_power: float Range: -145 to 20
		"""
		param = Conversions.decimal_value_to_str(reference_power)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:POWer:REFerence {param}')
