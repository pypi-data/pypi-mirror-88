from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Audio:
	"""Audio commands group definition. 7 total commands, 0 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("audio", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:STEReo:AUDio:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:AUDio:CATalog?')
		return Conversions.str_to_str_list(response)

	def set_dselect(self, dselect: str) -> None:
		"""[SOURce<HW>]:BB:STEReo:AUDio:DSELect \n
		No command help available \n
			:param dselect: No help available
		"""
		param = Conversions.value_to_quoted_str(dselect)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:AUDio:DSELect {param}')

	# noinspection PyTypeChecker
	def get_extclock(self) -> enums.FmStereoAudExtClk:
		"""[SOURce<HW>]:BB:STEReo:AUDio:EXTClock \n
		No command help available \n
			:return: ext_clock: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:AUDio:EXTClock?')
		return Conversions.str_to_scalar_enum(response, enums.FmStereoAudExtClk)

	def set_extclock(self, ext_clock: enums.FmStereoAudExtClk) -> None:
		"""[SOURce<HW>]:BB:STEReo:AUDio:EXTClock \n
		No command help available \n
			:param ext_clock: No help available
		"""
		param = Conversions.enum_scalar_to_str(ext_clock, enums.FmStereoAudExtClk)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:AUDio:EXTClock {param}')

	def get_level(self) -> float:
		"""[SOURce<HW>]:BB:STEReo:AUDio:LEVel \n
		No command help available \n
			:return: level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:AUDio:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""[SOURce<HW>]:BB:STEReo:AUDio:LEVel \n
		No command help available \n
			:param level: No help available
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:AUDio:LEVel {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FmStereoMode:
		"""[SOURce<HW>]:BB:STEReo:AUDio:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:AUDio:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FmStereoMode)

	def set_mode(self, mode: enums.FmStereoMode) -> None:
		"""[SOURce<HW>]:BB:STEReo:AUDio:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FmStereoMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:AUDio:MODE {param}')

	# noinspection PyTypeChecker
	def get_preemphasis(self) -> enums.FmStereoPreEmph:
		"""[SOURce<HW>]:BB:STEReo:AUDio:PREemphasis \n
		No command help available \n
			:return: pre_emphasis: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:AUDio:PREemphasis?')
		return Conversions.str_to_scalar_enum(response, enums.FmStereoPreEmph)

	def set_preemphasis(self, pre_emphasis: enums.FmStereoPreEmph) -> None:
		"""[SOURce<HW>]:BB:STEReo:AUDio:PREemphasis \n
		No command help available \n
			:param pre_emphasis: No help available
		"""
		param = Conversions.enum_scalar_to_str(pre_emphasis, enums.FmStereoPreEmph)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:AUDio:PREemphasis {param}')

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:BB:STEReo:AUDio:[FREQuency] \n
		No command help available \n
			:return: frequency: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:AUDio:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""[SOURce<HW>]:BB:STEReo:AUDio:[FREQuency] \n
		No command help available \n
			:param frequency: No help available
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:AUDio:FREQuency {param}')
