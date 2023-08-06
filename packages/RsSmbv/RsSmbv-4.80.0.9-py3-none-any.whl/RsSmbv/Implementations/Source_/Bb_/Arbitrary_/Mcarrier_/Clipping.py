from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clipping:
	"""Clipping commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clipping", core, parent)

	def get_cfactor(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CLIPping:CFACtor \n
		Sets the value of the desired crest factor, if baseband clipping is enabled. A target crest factor above the crest factor
		of the unclipped multicarrier signal has no effect. \n
			:return: cfactor: float Range: -50 to 50, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:CLIPping:CFACtor?')
		return Conversions.str_to_float(response)

	def set_cfactor(self, cfactor: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CLIPping:CFACtor \n
		Sets the value of the desired crest factor, if baseband clipping is enabled. A target crest factor above the crest factor
		of the unclipped multicarrier signal has no effect. \n
			:param cfactor: float Range: -50 to 50, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(cfactor)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CLIPping:CFACtor {param}')

	def get_cutoff(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CLIPping:CUToff \n
		Sets the cutoff frequency of the final low pass filter, if baseband clipping is enabled. \n
			:return: cutoff: float Range: 0 to 250E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:CLIPping:CUToff?')
		return Conversions.str_to_float(response)

	def set_cutoff(self, cutoff: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CLIPping:CUToff \n
		Sets the cutoff frequency of the final low pass filter, if baseband clipping is enabled. \n
			:param cutoff: float Range: 0 to 250E6
		"""
		param = Conversions.decimal_value_to_str(cutoff)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CLIPping:CUToff {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CLIPping:[STATe] \n
		Switches baseband clipping on and off. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:CLIPping:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CLIPping:[STATe] \n
		Switches baseband clipping on and off. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CLIPping:STATe {param}')
