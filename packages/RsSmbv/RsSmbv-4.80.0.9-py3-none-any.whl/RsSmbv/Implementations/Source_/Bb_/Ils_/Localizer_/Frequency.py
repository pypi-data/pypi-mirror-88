from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicCarrFreqMode:
		"""[SOURce<HW>]:[BB]:ILS:LOCalizer:FREQuency:MODE \n
		Sets the mode for the carrier frequency of the signal. \n
			:return: ils_loc_freq_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:LOCalizer:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicCarrFreqMode)

	def set_mode(self, ils_loc_freq_mode: enums.AvionicCarrFreqMode) -> None:
		"""[SOURce<HW>]:[BB]:ILS:LOCalizer:FREQuency:MODE \n
		Sets the mode for the carrier frequency of the signal. \n
			:param ils_loc_freq_mode: DECimal| ICAO DECimal Activates user-defined variation of the carrier frequency. ICAO Activates variation in predefined steps according to standard ILS transmitting frequencies (see Table 'ILS glide slope and localizer ICAO standard frequencies (MHz) and channels') .
		"""
		param = Conversions.enum_scalar_to_str(ils_loc_freq_mode, enums.AvionicCarrFreqMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:LOCalizer:FREQuency:MODE {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:[BB]:ILS:LOCalizer:FREQuency \n
		Sets the carrier frequency of the signal. \n
			:return: carrier_freq: float Range: 100E3 to 6E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:LOCalizer:FREQuency?')
		return Conversions.str_to_float(response)

	def set_value(self, carrier_freq: float) -> None:
		"""[SOURce<HW>]:[BB]:ILS:LOCalizer:FREQuency \n
		Sets the carrier frequency of the signal. \n
			:param carrier_freq: float Range: 100E3 to 6E9
		"""
		param = Conversions.decimal_value_to_str(carrier_freq)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:LOCalizer:FREQuency {param}')
