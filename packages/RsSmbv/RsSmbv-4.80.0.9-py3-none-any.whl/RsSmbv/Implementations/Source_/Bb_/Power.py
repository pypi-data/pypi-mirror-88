from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_peak(self) -> float:
		"""[SOURce<HW>]:BB:POWer:PEAK \n
		Queries the peak level of the baseband signal relative to full scale of 0.5 V (in terms of dB full scale) . \n
			:return: peak: float Range: -145 to 30, Unit: dBfs
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:POWer:PEAK?')
		return Conversions.str_to_float(response)

	def get_rms(self) -> float:
		"""[SOURce<HW>]:BB:POWer:RMS \n
		Queries the RMS level of the baseband signal relative to full scale of 0.5V (in terms of dB full scale) . \n
			:return: rms: float Range: -145 to 30, Unit: dBfs
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:POWer:RMS?')
		return Conversions.str_to_float(response)
