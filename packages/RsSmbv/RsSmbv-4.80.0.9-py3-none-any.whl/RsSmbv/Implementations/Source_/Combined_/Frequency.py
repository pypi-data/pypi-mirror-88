from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def get_start(self) -> float:
		"""[SOURce<HW>]:COMBined:FREQuency:STARt \n
		Sets the start frequency of the combined RF frequency / level sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:return: comb_freq_start: float Range: -59999E5 to 12E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:COMBined:FREQuency:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, comb_freq_start: float) -> None:
		"""[SOURce<HW>]:COMBined:FREQuency:STARt \n
		Sets the start frequency of the combined RF frequency / level sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:param comb_freq_start: float Range: -59999E5 to 12E9
		"""
		param = Conversions.decimal_value_to_str(comb_freq_start)
		self._core.io.write(f'SOURce<HwInstance>:COMBined:FREQuency:STARt {param}')

	def get_stop(self) -> float:
		"""[SOURce<HW>]:COMBined:FREQuency:STOP \n
		Sets the end frequency of the combined RF frequency / level sweep. \n
			:return: comb_freq_stop: float Range: -59999E5 to 12E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:COMBined:FREQuency:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, comb_freq_stop: float) -> None:
		"""[SOURce<HW>]:COMBined:FREQuency:STOP \n
		Sets the end frequency of the combined RF frequency / level sweep. \n
			:param comb_freq_stop: float Range: -59999E5 to 12E9
		"""
		param = Conversions.decimal_value_to_str(comb_freq_stop)
		self._core.io.write(f'SOURce<HwInstance>:COMBined:FREQuency:STOP {param}')
