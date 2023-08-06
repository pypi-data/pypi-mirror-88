from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mset:
	"""Mset commands group definition. 13 total commands, 0 Sub-groups, 13 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mset", core, parent)

	def get_boutput(self) -> bool:
		"""[SOURce<HW>]:BB:NFC:MSET:BOUTput \n
		When activated the signal at the baseband output changes between 0% and 100% voltage to be able to control the Reference
		Listeners. \n
			:return: boutput: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:BOUTput?')
		return Conversions.str_to_bool(response)

	def set_boutput(self, boutput: bool) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:BOUTput \n
		When activated the signal at the baseband output changes between 0% and 100% voltage to be able to control the Reference
		Listeners. \n
			:param boutput: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(boutput)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:BOUTput {param}')

	def get_brate(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:BRATe \n
		Returns the resulting bitrate for the current settings. \n
			:return: brate: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:BRATe?')
		return Conversions.str_to_float(response)

	def get_imodulation(self) -> bool:
		"""[SOURce<HW>]:BB:NFC:MSET:IMODulation \n
		When selected, inverse modulation will be used. \n
			:return: imodulation: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:IMODulation?')
		return Conversions.str_to_bool(response)

	def set_imodulation(self, imodulation: bool) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:IMODulation \n
		When selected, inverse modulation will be used. \n
			:param imodulation: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(imodulation)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:IMODulation {param}')

	def get_mdepth(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:MDEPth \n
		Sets the modulation depth in %. \n
			:return: mdepth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:MDEPth?')
		return Conversions.str_to_float(response)

	def set_mdepth(self, mdepth: float) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:MDEPth \n
		Sets the modulation depth in %. \n
			:param mdepth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(mdepth)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:MDEPth {param}')

	def get_mindex(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:MINDex \n
		Defines the signal's modulation index in %. \n
			:return: mi_ndex: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:MINDex?')
		return Conversions.str_to_float(response)

	def set_mindex(self, mi_ndex: float) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:MINDex \n
		Defines the signal's modulation index in %. \n
			:param mi_ndex: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(mi_ndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:MINDex {param}')

	def get_osrise(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:OSRise \n
		Determines the size of the overshoot after the rising slope. \n
			:return: orise: float Range: 0 to 42
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:OSRise?')
		return Conversions.str_to_float(response)

	def set_osrise(self, orise: float) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:OSRise \n
		Determines the size of the overshoot after the rising slope. \n
			:param orise: float Range: 0 to 42
		"""
		param = Conversions.decimal_value_to_str(orise)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:OSRise {param}')

	def get_rcurve(self) -> bool:
		"""[SOURce<HW>]:BB:NFC:MSET:RCURve \n
		When activated an 'RLC curve' is applied to the signal, otherwise a linear ramp is used. \n
			:return: rcurve: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:RCURve?')
		return Conversions.str_to_bool(response)

	def set_rcurve(self, rcurve: bool) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:RCURve \n
		When activated an 'RLC curve' is applied to the signal, otherwise a linear ramp is used. \n
			:param rcurve: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(rcurve)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:RCURve {param}')

	def get_slope(self) -> bool:
		"""[SOURce<HW>]:BB:NFC:MSET:SLOPe \n
		Determines the transition between the modulated and unmodulated parts (Edge/Slope) . \n
			:return: eslope: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:SLOPe?')
		return Conversions.str_to_bool(response)

	def set_slope(self, eslope: bool) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:SLOPe \n
		Determines the transition between the modulated and unmodulated parts (Edge/Slope) . \n
			:param eslope: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(eslope)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:SLOPe {param}')

	def get_symbol_rate(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:SRATe \n
		Enters the sample rate, i.e. the time resolution of the generated signal. \n
			:return: srate: float Range: depends on protocol mode to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:SRATe?')
		return Conversions.str_to_float(response)

	def set_symbol_rate(self, srate: float) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:SRATe \n
		Enters the sample rate, i.e. the time resolution of the generated signal. \n
			:param srate: float Range: depends on protocol mode to dynamic
		"""
		param = Conversions.decimal_value_to_str(srate)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:SRATe {param}')

	def get_tfall(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:TFALl \n
		Defines the fall time (90 to 5 %) in μs. \n
			:return: tfall: float Range: 0 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:TFALl?')
		return Conversions.str_to_float(response)

	def set_tfall(self, tfall: float) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:TFALl \n
		Defines the fall time (90 to 5 %) in μs. \n
			:param tfall: float Range: 0 to dynamic
		"""
		param = Conversions.decimal_value_to_str(tfall)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:TFALl {param}')

	def get_tlow(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:TLOW \n
		Defines the signals low time (below 5%) in µs. \n
			:return: tlow: float Range: 0.4 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:TLOW?')
		return Conversions.str_to_float(response)

	def set_tlow(self, tlow: float) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:TLOW \n
		Defines the signals low time (below 5%) in µs. \n
			:param tlow: float Range: 0.4 to dynamic
		"""
		param = Conversions.decimal_value_to_str(tlow)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:TLOW {param}')

	def get_trise(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:TRISe \n
		Defines the signals rise time (5 to 90 %) in μs. \n
			:return: trise: float Range: dynamic to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:TRISe?')
		return Conversions.str_to_float(response)

	def set_trise(self, trise: float) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:TRISe \n
		Defines the signals rise time (5 to 90 %) in μs. \n
			:param trise: float Range: dynamic to dynamic
		"""
		param = Conversions.decimal_value_to_str(trise)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:TRISe {param}')

	def get_usfall(self) -> float:
		"""[SOURce<HW>]:BB:NFC:MSET:USFall \n
		Determines the size of the undershoot (ringing) after the falling slope. \n
			:return: ofall: float Range: 0 to 42
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:MSET:USFall?')
		return Conversions.str_to_float(response)

	def set_usfall(self, ofall: float) -> None:
		"""[SOURce<HW>]:BB:NFC:MSET:USFall \n
		Determines the size of the undershoot (ringing) after the falling slope. \n
			:param ofall: float Range: 0 to 42
		"""
		param = Conversions.decimal_value_to_str(ofall)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:MSET:USFall {param}')
