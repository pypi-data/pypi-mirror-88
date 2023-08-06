from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_start(self) -> float:
		"""[SOURce<HW>]:COMBined:POWer:STARt \n
		Sets the start level value of the combined RF frequency / level sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:return: comb_pow_start: float Range: -245 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:COMBined:POWer:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, comb_pow_start: float) -> None:
		"""[SOURce<HW>]:COMBined:POWer:STARt \n
		Sets the start level value of the combined RF frequency / level sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:param comb_pow_start: float Range: -245 to 120
		"""
		param = Conversions.decimal_value_to_str(comb_pow_start)
		self._core.io.write(f'SOURce<HwInstance>:COMBined:POWer:STARt {param}')

	def get_stop(self) -> float:
		"""[SOURce<HW>]:COMBined:POWer:STOP \n
		Sets the stop level value of the combined RF frequency / level sweep. \n
			:return: comb_pow_stop: float Range: -245 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:COMBined:POWer:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, comb_pow_stop: float) -> None:
		"""[SOURce<HW>]:COMBined:POWer:STOP \n
		Sets the stop level value of the combined RF frequency / level sweep. \n
			:param comb_pow_stop: float Range: -245 to 120
		"""
		param = Conversions.decimal_value_to_str(comb_pow_stop)
		self._core.io.write(f'SOURce<HwInstance>:COMBined:POWer:STOP {param}')
