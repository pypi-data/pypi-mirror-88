from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpch:
	"""Dpch commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpch", core, parent)

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:UP:PPARameter:DPCH:COUNt \n
		Sets the number of activated DPCHs. The maximum number depends on the spreading factor: Max. No. DPCH = 3 x 'Spreading
		Factor' \n
			:return: count: integer Range: 1 to 48
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:UP:PPARameter:DPCH:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:UP:PPARameter:DPCH:COUNt \n
		Sets the number of activated DPCHs. The maximum number depends on the spreading factor: Max. No. DPCH = 3 x 'Spreading
		Factor' \n
			:param count: integer Range: 1 to 48
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:PPARameter:DPCH:COUNt {param}')

	# noinspection PyTypeChecker
	def get_crest(self) -> enums.CresFactMode:
		"""[SOURce<HW>]:BB:TDSCdma:UP:PPARameter:DPCH:CRESt \n
		Selects the desired range for the crest factor of the test scenario. \n
			:return: crest: MINimum| AVERage| WORSt MINimum The crest factor is minimized. The channelization codes are distributed uniformly over the code domain. The timing offsets are increased by 3 per channel. AVERage An average crest factor is set. The channelization codes are distributed uniformly over the code domain. The timing offsets are all set to 0. WORSt The crest factor is set to an unfavorable value (i.e. maximum) . The channelization codes are assigned in ascending order. The timing offsets are all set to 0.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:UP:PPARameter:DPCH:CRESt?')
		return Conversions.str_to_scalar_enum(response, enums.CresFactMode)

	def set_crest(self, crest: enums.CresFactMode) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:UP:PPARameter:DPCH:CRESt \n
		Selects the desired range for the crest factor of the test scenario. \n
			:param crest: MINimum| AVERage| WORSt MINimum The crest factor is minimized. The channelization codes are distributed uniformly over the code domain. The timing offsets are increased by 3 per channel. AVERage An average crest factor is set. The channelization codes are distributed uniformly over the code domain. The timing offsets are all set to 0. WORSt The crest factor is set to an unfavorable value (i.e. maximum) . The channelization codes are assigned in ascending order. The timing offsets are all set to 0.
		"""
		param = Conversions.enum_scalar_to_str(crest, enums.CresFactMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:PPARameter:DPCH:CRESt {param}')

	# noinspection PyTypeChecker
	def get_sfactor(self) -> enums.TdscdmaSpreadFactor:
		"""[SOURce<HW>]:BB:TDSCdma:UP:PPARameter:DPCH:SFACtor \n
		Sets the spreading factor for the DPCHs. \n
			:return: sfactor: 1| 2| 4| 8| 16
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:UP:PPARameter:DPCH:SFACtor?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaSpreadFactor)

	def set_sfactor(self, sfactor: enums.TdscdmaSpreadFactor) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:UP:PPARameter:DPCH:SFACtor \n
		Sets the spreading factor for the DPCHs. \n
			:param sfactor: 1| 2| 4| 8| 16
		"""
		param = Conversions.enum_scalar_to_str(sfactor, enums.TdscdmaSpreadFactor)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:PPARameter:DPCH:SFACtor {param}')
