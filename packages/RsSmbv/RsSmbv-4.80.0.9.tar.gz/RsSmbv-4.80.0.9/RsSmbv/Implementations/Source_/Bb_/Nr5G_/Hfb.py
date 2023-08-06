from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hfb:
	"""Hfb commands group definition. 11 total commands, 0 Sub-groups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hfb", core, parent)

	def get_adj_cmd(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:HFB:ADJCmd \n
		No command help available \n
			:return: init_timing_adj_cm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:ADJCmd?')
		return Conversions.str_to_int(response)

	def set_adj_cmd(self, init_timing_adj_cm: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:ADJCmd \n
		No command help available \n
			:param init_timing_adj_cm: No help available
		"""
		param = Conversions.decimal_value_to_str(init_timing_adj_cm)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:ADJCmd {param}')

	def get_baseband(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:HFB:BASeband \n
		No command help available \n
			:return: fb_baseband: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:BASeband?')
		return Conversions.str_to_int(response)

	def set_baseband(self, fb_baseband: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:BASeband \n
		No command help available \n
			:param fb_baseband: No help available
		"""
		param = Conversions.decimal_value_to_str(fb_baseband)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:BASeband {param}')

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.FeedbackConnectorAll:
		"""[SOURce<HW>]:BB:NR5G:HFB:CONNector \n
		No command help available \n
			:return: fb_connector: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.FeedbackConnectorAll)

	def set_connector(self, fb_connector: enums.FeedbackConnectorAll) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:CONNector \n
		No command help available \n
			:param fb_connector: No help available
		"""
		param = Conversions.enum_scalar_to_str(fb_connector, enums.FeedbackConnectorAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:CONNector {param}')

	def get_delay(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:HFB:DELay \n
		No command help available \n
			:return: fb_user_delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, fb_user_delay: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:DELay \n
		No command help available \n
			:param fb_user_delay: No help available
		"""
		param = Conversions.decimal_value_to_str(fb_user_delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:DELay {param}')

	def get_hpn_mode(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:HFB:HPNMode \n
		No command help available \n
			:return: hpn_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:HPNMode?')
		return Conversions.str_to_bool(response)

	def set_hpn_mode(self, hpn_mode: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:HPNMode \n
		No command help available \n
			:param hpn_mode: No help available
		"""
		param = Conversions.bool_to_str(hpn_mode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:HPNMode {param}')

	def get_log_path(self) -> str:
		"""[SOURce<HW>]:BB:NR5G:HFB:LOGPath \n
		No command help available \n
			:return: log_gen_outp_path: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:LOGPath?')
		return trim_str_response(response)

	def set_log_path(self, log_gen_outp_path: str) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:LOGPath \n
		No command help available \n
			:param log_gen_outp_path: No help available
		"""
		param = Conversions.value_to_quoted_str(log_gen_outp_path)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:LOGPath {param}')

	def get_log_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:HFB:LOGState \n
		No command help available \n
			:return: log_gen_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:LOGState?')
		return Conversions.str_to_bool(response)

	def set_log_state(self, log_gen_state: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:LOGState \n
		No command help available \n
			:param log_gen_state: No help available
		"""
		param = Conversions.bool_to_str(log_gen_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:LOGState {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FeedbackModeAll:
		"""[SOURce<HW>]:BB:NR5G:HFB:MODE \n
		No command help available \n
			:return: fb_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FeedbackModeAll)

	def set_mode(self, fb_mode: enums.FeedbackModeAll) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:MODE \n
		No command help available \n
			:param fb_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(fb_mode, enums.FeedbackModeAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:MODE {param}')

	def get_pdelay(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:HFB:PDELay \n
		No command help available \n
			:return: processing_delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:PDELay?')
		return Conversions.str_to_float(response)

	def set_pdelay(self, processing_delay: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:PDELay \n
		No command help available \n
			:param processing_delay: No help available
		"""
		param = Conversions.decimal_value_to_str(processing_delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:PDELay {param}')

	# noinspection PyTypeChecker
	def get_symbol_rate(self) -> enums.FeedbackRateAll:
		"""[SOURce<HW>]:BB:NR5G:HFB:SRATe \n
		No command help available \n
			:return: fb_serial_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:SRATe?')
		return Conversions.str_to_scalar_enum(response, enums.FeedbackRateAll)

	def set_symbol_rate(self, fb_serial_rate: enums.FeedbackRateAll) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:SRATe \n
		No command help available \n
			:param fb_serial_rate: No help available
		"""
		param = Conversions.enum_scalar_to_str(fb_serial_rate, enums.FeedbackRateAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:SRATe {param}')

	def get_ta_mode(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:HFB:TAMode \n
		No command help available \n
			:return: ta_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:TAMode?')
		return Conversions.str_to_bool(response)

	def set_ta_mode(self, ta_mode: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:HFB:TAMode \n
		No command help available \n
			:param ta_mode: No help available
		"""
		param = Conversions.bool_to_str(ta_mode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:TAMode {param}')
