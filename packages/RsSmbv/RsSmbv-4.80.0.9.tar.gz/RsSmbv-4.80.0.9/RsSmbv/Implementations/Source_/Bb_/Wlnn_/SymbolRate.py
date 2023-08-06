from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def get_variation(self) -> float:
		"""[SOURce<HW>]:BB:WLNN:SRATe:VARiation \n
		Sets the sample rate of the signal. \n
			:return: variation: float Range: 400 to 40000000, Unit: Hz (c/s)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:SRATe:VARiation?')
		return Conversions.str_to_float(response)

	def set_variation(self, variation: float) -> None:
		"""[SOURce<HW>]:BB:WLNN:SRATe:VARiation \n
		Sets the sample rate of the signal. \n
			:param variation: float Range: 400 to 40000000, Unit: Hz (c/s)
		"""
		param = Conversions.decimal_value_to_str(variation)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:SRATe:VARiation {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:BB:WLNN:SRATe \n
		Displays the sample rate specific for the selected bandwidth (method RsSmbv.Source.Bb.Wlnn.bandwidth) . \n
			:return: samp_rate: float 20MHz for BW20, 60MHz for BW40.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:SRATe?')
		return Conversions.str_to_float(response)
