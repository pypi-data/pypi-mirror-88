from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spc:
	"""Spc commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spc", core, parent)

	def get_crange(self) -> float:
		"""[SOURce<HW>]:POWer:SPC:CRANge \n
		No command help available \n
			:return: pow_cntrl_cr_ange: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:CRANge?')
		return Conversions.str_to_float(response)

	def set_crange(self, pow_cntrl_cr_ange: float) -> None:
		"""[SOURce<HW>]:POWer:SPC:CRANge \n
		No command help available \n
			:param pow_cntrl_cr_ange: No help available
		"""
		param = Conversions.decimal_value_to_str(pow_cntrl_cr_ange)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:CRANge {param}')

	def get_delay(self) -> int:
		"""[SOURce<HW>]:POWer:SPC:DELay \n
		No command help available \n
			:return: pow_cntrl_delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:DELay?')
		return Conversions.str_to_int(response)

	def set_delay(self, pow_cntrl_delay: int) -> None:
		"""[SOURce<HW>]:POWer:SPC:DELay \n
		No command help available \n
			:param pow_cntrl_delay: No help available
		"""
		param = Conversions.decimal_value_to_str(pow_cntrl_delay)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:DELay {param}')

	def get_peak(self) -> bool:
		"""[SOURce<HW>]:POWer:SPC:PEAK \n
		No command help available \n
			:return: pow_cntrl_peak: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:PEAK?')
		return Conversions.str_to_bool(response)

	def set_peak(self, pow_cntrl_peak: bool) -> None:
		"""[SOURce<HW>]:POWer:SPC:PEAK \n
		No command help available \n
			:param pow_cntrl_peak: No help available
		"""
		param = Conversions.bool_to_str(pow_cntrl_peak)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:PEAK {param}')

	# noinspection PyTypeChecker
	def get_select(self) -> enums.PowCntrlSelect:
		"""[SOURce<HW>]:POWer:SPC:SELect \n
		No command help available \n
			:return: pow_cntrl_select: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:SELect?')
		return Conversions.str_to_scalar_enum(response, enums.PowCntrlSelect)

	def set_select(self, pow_cntrl_select: enums.PowCntrlSelect) -> None:
		"""[SOURce<HW>]:POWer:SPC:SELect \n
		No command help available \n
			:param pow_cntrl_select: No help available
		"""
		param = Conversions.enum_scalar_to_str(pow_cntrl_select, enums.PowCntrlSelect)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:SELect {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:POWer:SPC:STATe \n
		No command help available \n
			:return: pow_cntrl_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, pow_cntrl_state: bool) -> None:
		"""[SOURce<HW>]:POWer:SPC:STATe \n
		No command help available \n
			:param pow_cntrl_state: No help available
		"""
		param = Conversions.bool_to_str(pow_cntrl_state)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:STATe {param}')

	def get_target(self) -> float:
		"""[SOURce<HW>]:POWer:SPC:TARGet \n
		No command help available \n
			:return: pow_cntrl_target: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:TARGet?')
		return Conversions.str_to_float(response)

	def set_target(self, pow_cntrl_target: float) -> None:
		"""[SOURce<HW>]:POWer:SPC:TARGet \n
		No command help available \n
			:param pow_cntrl_target: No help available
		"""
		param = Conversions.decimal_value_to_str(pow_cntrl_target)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:TARGet {param}')
