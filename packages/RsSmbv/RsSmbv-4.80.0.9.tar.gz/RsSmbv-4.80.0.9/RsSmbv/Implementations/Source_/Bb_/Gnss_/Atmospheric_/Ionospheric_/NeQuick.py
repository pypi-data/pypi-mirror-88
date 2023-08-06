from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NeQuick:
	"""NeQuick commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("neQuick", core, parent)

	def get_sflux(self) -> float:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:NEQuick:SFLux \n
		Sets the solar flux level. \n
			:return: solar_flux: float Range: 0 to 300
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:NEQuick:SFLux?')
		return Conversions.str_to_float(response)

	def set_sflux(self, solar_flux: float) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:NEQuick:SFLux \n
		Sets the solar flux level. \n
			:param solar_flux: float Range: 0 to 300
		"""
		param = Conversions.decimal_value_to_str(solar_flux)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:NEQuick:SFLux {param}')

	def get_sun_spot(self) -> float:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:NEQuick:SUNSpot \n
		Sets the sunspot number. \n
			:return: sunspot_number: float Range: -99.636 to 248.870
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:NEQuick:SUNSpot?')
		return Conversions.str_to_float(response)

	def set_sun_spot(self, sunspot_number: float) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:NEQuick:SUNSpot \n
		Sets the sunspot number. \n
			:param sunspot_number: float Range: -99.636 to 248.870
		"""
		param = Conversions.decimal_value_to_str(sunspot_number)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:NEQuick:SUNSpot {param}')

	def get_umsn(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:NEQuick:UMSN \n
		Enables the instrument to use the measured sunspot number value. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:NEQuick:UMSN?')
		return Conversions.str_to_bool(response)

	def set_umsn(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:NEQuick:UMSN \n
		Enables the instrument to use the measured sunspot number value. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:NEQuick:UMSN {param}')
