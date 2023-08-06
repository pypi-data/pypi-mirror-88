from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Optimization:
	"""Optimization commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("optimization", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.OptimizationMode:
		"""[SOURce<HW>]:BB:IMPairment:OPTimization:MODE \n
		Sets the optimization mode. \n
			:return: mode: FAST| | QHIGh FAST Optimization by compensation for I/Q skew. QHIGh Optimization by compensation for I/Q skew and frequency response correction. This mode interrupts the RF signal. Do not use it in combination with the uninterrupted level settings and strictly monotone modes RF level modes. (See method RsSmbv.Source.Power.lbehaviour.)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IMPairment:OPTimization:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.OptimizationMode)

	def set_mode(self, mode: enums.OptimizationMode) -> None:
		"""[SOURce<HW>]:BB:IMPairment:OPTimization:MODE \n
		Sets the optimization mode. \n
			:param mode: FAST| | QHIGh FAST Optimization by compensation for I/Q skew. QHIGh Optimization by compensation for I/Q skew and frequency response correction. This mode interrupts the RF signal. Do not use it in combination with the uninterrupted level settings and strictly monotone modes RF level modes. (See method RsSmbv.Source.Power.lbehaviour.)
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.OptimizationMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:IMPairment:OPTimization:MODE {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:IMPairment:OPTimization:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IMPairment:OPTimization:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:IMPairment:OPTimization:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:IMPairment:OPTimization:STATe {param}')
