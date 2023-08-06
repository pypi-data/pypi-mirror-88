from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Threshold:
	"""Threshold commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("threshold", core, parent)

	def get_all(self) -> float:
		"""[SOURce<HW>]:DM:THReshold:[ALL] \n
		No command help available \n
			:return: threshold: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DM:THReshold:ALL?')
		return Conversions.str_to_float(response)

	def set_all(self, threshold: float) -> None:
		"""[SOURce<HW>]:DM:THReshold:[ALL] \n
		No command help available \n
			:param threshold: No help available
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'SOURce<HwInstance>:DM:THReshold:ALL {param}')
