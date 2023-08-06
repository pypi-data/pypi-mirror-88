from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lte:
	"""Lte commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lte", core, parent)

	def get_coffactor(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:LTE:COFFactor \n
		Sets the cut-off frequency factor for the LTE filter type. \n
			:return: cutoff_factor: float Range: 0.02 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:LTE:COFFactor?')
		return Conversions.str_to_float(response)

	def set_coffactor(self, cutoff_factor: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:LTE:COFFactor \n
		Sets the cut-off frequency factor for the LTE filter type. \n
			:param cutoff_factor: float Range: 0.02 to 2
		"""
		param = Conversions.decimal_value_to_str(cutoff_factor)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:LTE:COFFactor {param}')

	def get_cofs(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:LTE:COFS \n
		Sets the cut-off frequency shift of the applied filter. \n
			:return: cut_off_freq_shift: float Range: -1 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:LTE:COFS?')
		return Conversions.str_to_float(response)

	def set_cofs(self, cut_off_freq_shift: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:LTE:COFS \n
		Sets the cut-off frequency shift of the applied filter. \n
			:param cut_off_freq_shift: float Range: -1 to 1
		"""
		param = Conversions.decimal_value_to_str(cut_off_freq_shift)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:LTE:COFS {param}')

	# noinspection PyTypeChecker
	def get_optimization(self) -> enums.FiltOptType:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:LTE:OPTimization \n
		Defines the applied LTE filter. \n
			:return: optimization: EVM| STD| ACP| ACPN| BENU
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:LTE:OPTimization?')
		return Conversions.str_to_scalar_enum(response, enums.FiltOptType)

	def set_optimization(self, optimization: enums.FiltOptType) -> None:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:LTE:OPTimization \n
		Defines the applied LTE filter. \n
			:param optimization: EVM| STD| ACP| ACPN| BENU
		"""
		param = Conversions.enum_scalar_to_str(optimization, enums.FiltOptType)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:LTE:OPTimization {param}')

	def get_ro_factor(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:LTE:ROFactor \n
		Sets the roll-off factor for the LTE filter type. \n
			:return: roll_off_factor: float Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:LTE:ROFactor?')
		return Conversions.str_to_float(response)

	def set_ro_factor(self, roll_off_factor: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:FILTer:PARameter:LTE:ROFactor \n
		Sets the roll-off factor for the LTE filter type. \n
			:param roll_off_factor: float Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(roll_off_factor)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FILTer:PARameter:LTE:ROFactor {param}')
