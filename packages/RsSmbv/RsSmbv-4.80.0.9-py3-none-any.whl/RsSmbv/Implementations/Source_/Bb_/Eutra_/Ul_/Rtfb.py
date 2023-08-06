from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rtfb:
	"""Rtfb commands group definition. 16 total commands, 0 Sub-groups, 16 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rtfb", core, parent)

	def get_aack(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:AACK \n
		No command help available \n
			:return: assume_ack: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:AACK?')
		return Conversions.str_to_bool(response)

	def set_aack(self, assume_ack: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:AACK \n
		No command help available \n
			:param assume_ack: No help available
		"""
		param = Conversions.bool_to_str(assume_ack)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:AACK {param}')

	# noinspection PyTypeChecker
	def get_ack_definition(self) -> enums.LowHigh:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:ACKDefinition \n
		No command help available \n
			:return: ack_definition: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:ACKDefinition?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_ack_definition(self, ack_definition: enums.LowHigh) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:ACKDefinition \n
		No command help available \n
			:param ack_definition: No help available
		"""
		param = Conversions.enum_scalar_to_str(ack_definition, enums.LowHigh)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:ACKDefinition {param}')

	def get_adu_delay(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:ADUDelay \n
		No command help available \n
			:return: add_user_delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:ADUDelay?')
		return Conversions.str_to_float(response)

	def set_adu_delay(self, add_user_delay: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:ADUDelay \n
		No command help available \n
			:param add_user_delay: No help available
		"""
		param = Conversions.decimal_value_to_str(add_user_delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:ADUDelay {param}')

	def get_bb_selector(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:BBSelector \n
		No command help available \n
			:return: baseband_select: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:BBSelector?')
		return Conversions.str_to_int(response)

	def set_bb_selector(self, baseband_select: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:BBSelector \n
		No command help available \n
			:param baseband_select: No help available
		"""
		param = Conversions.decimal_value_to_str(baseband_select)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:BBSelector {param}')

	# noinspection PyTypeChecker
	def get_be_insertion(self) -> enums.EutraFeedbackBlerMode:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:BEINsertion \n
		No command help available \n
			:return: block_err_insert: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:BEINsertion?')
		return Conversions.str_to_scalar_enum(response, enums.EutraFeedbackBlerMode)

	def set_be_insertion(self, block_err_insert: enums.EutraFeedbackBlerMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:BEINsertion \n
		No command help available \n
			:param block_err_insert: No help available
		"""
		param = Conversions.enum_scalar_to_str(block_err_insert, enums.EutraFeedbackBlerMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:BEINsertion {param}')

	def get_bit_error_rate(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:BERate \n
		No command help available \n
			:return: block_err_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:BERate?')
		return Conversions.str_to_float(response)

	def set_bit_error_rate(self, block_err_rate: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:BERate \n
		No command help available \n
			:param block_err_rate: No help available
		"""
		param = Conversions.decimal_value_to_str(block_err_rate)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:BERate {param}')

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.FeedbackConnector:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:CONNector \n
		No command help available \n
			:return: connector: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.FeedbackConnector)

	def set_connector(self, connector: enums.FeedbackConnector) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:CONNector \n
		No command help available \n
			:param connector: No help available
		"""
		param = Conversions.enum_scalar_to_str(connector, enums.FeedbackConnector)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:CONNector {param}')

	# noinspection PyTypeChecker
	def get_dmode(self) -> enums.EutraFeedbackDistMode:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:DMODe \n
		No command help available \n
			:return: distance_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:DMODe?')
		return Conversions.str_to_scalar_enum(response, enums.EutraFeedbackDistMode)

	def set_dmode(self, distance_mode: enums.EutraFeedbackDistMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:DMODe \n
		No command help available \n
			:param distance_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(distance_mode, enums.EutraFeedbackDistMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:DMODe {param}')

	def get_gen_reports(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:GENReports \n
		No command help available \n
			:return: gen_debug_reports: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:GENReports?')
		return Conversions.str_to_bool(response)

	def set_gen_reports(self, gen_debug_reports: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:GENReports \n
		No command help available \n
			:param gen_debug_reports: No help available
		"""
		param = Conversions.bool_to_str(gen_debug_reports)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:GENReports {param}')

	def get_it_advance(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:ITADvance \n
		No command help available \n
			:return: init_tim_advance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:ITADvance?')
		return Conversions.str_to_int(response)

	def set_it_advance(self, init_tim_advance: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:ITADvance \n
		No command help available \n
			:param init_tim_advance: No help available
		"""
		param = Conversions.decimal_value_to_str(init_tim_advance)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:ITADvance {param}')

	def get_ita_feedback(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:ITAFeedback \n
		No command help available \n
			:return: ignore_timing_adj: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:ITAFeedback?')
		return Conversions.str_to_bool(response)

	def set_ita_feedback(self, ignore_timing_adj: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:ITAFeedback \n
		No command help available \n
			:param ignore_timing_adj: No help available
		"""
		param = Conversions.bool_to_str(ignore_timing_adj)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:ITAFeedback {param}')

	def get_loffset(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:LOFFset \n
		No command help available \n
			:return: logging_offs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:LOFFset?')
		return Conversions.str_to_int(response)

	def set_loffset(self, logging_offs: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:LOFFset \n
		No command help available \n
			:param logging_offs: No help available
		"""
		param = Conversions.decimal_value_to_str(logging_offs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:LOFFset {param}')

	def get_max_trans(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:MAXTrans \n
		No command help available \n
			:return: max_transmission: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:MAXTrans?')
		return Conversions.str_to_int(response)

	def set_max_trans(self, max_transmission: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:MAXTrans \n
		No command help available \n
			:param max_transmission: No help available
		"""
		param = Conversions.decimal_value_to_str(max_transmission)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:MAXTrans {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.EutraFeedbackMode:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraFeedbackMode)

	def set_mode(self, mode: enums.EutraFeedbackMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.EutraFeedbackMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:MODE {param}')

	def get_rv_sequence(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:RVSequence \n
		No command help available \n
			:return: red_vers_sequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:RVSequence?')
		return trim_str_response(response)

	def set_rv_sequence(self, red_vers_sequence: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:RVSequence \n
		No command help available \n
			:param red_vers_sequence: No help available
		"""
		param = Conversions.value_to_quoted_str(red_vers_sequence)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:RVSequence {param}')

	# noinspection PyTypeChecker
	def get_ser_rte(self) -> enums.EutraSerialRate:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:SERate \n
		No command help available \n
			:return: serial_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:RTFB:SERate?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSerialRate)

	def set_ser_rte(self, serial_rate: enums.EutraSerialRate) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:RTFB:SERate \n
		No command help available \n
			:param serial_rate: No help available
		"""
		param = Conversions.enum_scalar_to_str(serial_rate, enums.EutraSerialRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:RTFB:SERate {param}')
