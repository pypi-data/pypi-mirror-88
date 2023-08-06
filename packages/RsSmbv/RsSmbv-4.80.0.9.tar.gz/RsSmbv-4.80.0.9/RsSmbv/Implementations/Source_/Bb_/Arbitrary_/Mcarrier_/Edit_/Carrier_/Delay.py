from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def get_step(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:EDIT:CARRier:DELay:STEP \n
		Sets the step width by which the start delays of the carriers in the defined carrier range is incremented. \n
			:return: step: float Range: -1 to 1, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:EDIT:CARRier:DELay:STEP?')
		return Conversions.str_to_float(response)

	def set_step(self, step: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:EDIT:CARRier:DELay:STEP \n
		Sets the step width by which the start delays of the carriers in the defined carrier range is incremented. \n
			:param step: float Range: -1 to 1, Unit: s
		"""
		param = Conversions.decimal_value_to_str(step)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:EDIT:CARRier:DELay:STEP {param}')

	def get_start(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:EDIT:CARRier:DELay:[STARt] \n
		Sets the start delay for the individual carriers in the defined carrier range. \n
			:return: start: float Range: 0 to 1, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:EDIT:CARRier:DELay:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:EDIT:CARRier:DELay:[STARt] \n
		Sets the start delay for the individual carriers in the defined carrier range. \n
			:param start: float Range: 0 to 1, Unit: s
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:EDIT:CARRier:DELay:STARt {param}')
