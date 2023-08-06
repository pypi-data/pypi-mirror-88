from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ppst:
	"""Ppst commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ppst", core, parent)

	def get_enabled(self) -> bool:
		"""[SOURce<HW>]:BB:DME:PPST:ENABled \n
		Enables the pulse pair spacing tolerance. If this function is not enabled, the response is sent after the first pulse,
		without checking whether the second pulse is within the pulse pair spacing tolerance time. You can set the pulse pair
		spacing tolerance with [:SOURce<hw>][:BB]:DME:PPST. \n
			:return: toler_enabled: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PPST:ENABled?')
		return Conversions.str_to_bool(response)

	def set_enabled(self, toler_enabled: bool) -> None:
		"""[SOURce<HW>]:BB:DME:PPST:ENABled \n
		Enables the pulse pair spacing tolerance. If this function is not enabled, the response is sent after the first pulse,
		without checking whether the second pulse is within the pulse pair spacing tolerance time. You can set the pulse pair
		spacing tolerance with [:SOURce<hw>][:BB]:DME:PPST. \n
			:param toler_enabled: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(toler_enabled)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PPST:ENABled {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:PPST \n
		Sets the pulse pair spacing tolerance. You have to enable the pulse pair spacing tolerance with the command method RsSmbv.
		Source.Bb.Dme.pps for this value to be considered. \n
			:return: spac_tolerance: float Range: 0 to (200E-6) /2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PPST?')
		return Conversions.str_to_float(response)

	def set_value(self, spac_tolerance: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:PPST \n
		Sets the pulse pair spacing tolerance. You have to enable the pulse pair spacing tolerance with the command method RsSmbv.
		Source.Bb.Dme.pps for this value to be considered. \n
			:param spac_tolerance: float Range: 0 to (200E-6) /2
		"""
		param = Conversions.decimal_value_to_str(spac_tolerance)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PPST {param}')
