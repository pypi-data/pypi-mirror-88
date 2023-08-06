from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def get_max(self) -> int:
		"""[SOURce<HW>]:BBIN:SRATe:MAX \n
		Queries the maximum sample rate. \n
			:return: dig_iq_hs_out_sr_max: integer Range: 400 to 600E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:SRATe:MAX?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.BbinSampRateMode:
		"""[SOURce<HW>]:BBIN:SRATe:SOURce \n
		Sets the digital interface used to estimate the sample rate. \n
			:return: source: DIN | HSDin DIN Estimates the sample rate based on the digital input signal. HSDin Enabled for method RsSmbv.Source.Bbin.Digital.interfaceHSDin.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:SRATe:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.BbinSampRateMode)

	def set_source(self, source: enums.BbinSampRateMode) -> None:
		"""[SOURce<HW>]:BBIN:SRATe:SOURce \n
		Sets the digital interface used to estimate the sample rate. \n
			:param source: DIN | HSDin DIN Estimates the sample rate based on the digital input signal. HSDin Enabled for method RsSmbv.Source.Bbin.Digital.interfaceHSDin.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.BbinSampRateMode)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:SRATe:SOURce {param}')

	def get_sum(self) -> int:
		"""[SOURce<HW>]:BBIN:SRATe:SUM \n
		Queries the sum of the sample rates of all active channels. \n
			:return: dig_iq_hs_out_sr_sum: integer Range: 0 to depends on settings
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:SRATe:SUM?')
		return Conversions.str_to_int(response)

	def get_actual(self) -> float:
		"""[SOURce<HW>]:BBIN:SRATe:[ACTual] \n
		Queries the sample rate of the external digital baseband signal. \n
			:return: actual: float Range: 400 to 100E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:SRATe:ACTual?')
		return Conversions.str_to_float(response)

	def set_actual(self, actual: float) -> None:
		"""[SOURce<HW>]:BBIN:SRATe:[ACTual] \n
		Queries the sample rate of the external digital baseband signal. \n
			:param actual: float Range: 400 to 100E6
		"""
		param = Conversions.decimal_value_to_str(actual)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:SRATe:ACTual {param}')
