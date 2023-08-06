from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rtf:
	"""Rtf commands group definition. 10 total commands, 0 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rtf", core, parent)

	# noinspection PyTypeChecker
	def get_ack_definition(self) -> enums.LowHigh:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:ACKDefinition \n
		No command help available \n
			:return: ack_definition: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:ACKDefinition?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_ack_definition(self, ack_definition: enums.LowHigh) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:ACKDefinition \n
		No command help available \n
			:param ack_definition: No help available
		"""
		param = Conversions.enum_scalar_to_str(ack_definition, enums.LowHigh)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:ACKDefinition {param}')

	def get_aus_delay(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:AUSDelay \n
		No command help available \n
			:return: add_user_delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:AUSDelay?')
		return Conversions.str_to_float(response)

	def set_aus_delay(self, add_user_delay: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:AUSDelay \n
		No command help available \n
			:param add_user_delay: No help available
		"""
		param = Conversions.decimal_value_to_str(add_user_delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:AUSDelay {param}')

	def get_bb_smue(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:BBSMue \n
		No command help available \n
			:return: bb_select_mov_ue: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:BBSMue?')
		return Conversions.str_to_int(response)

	def set_bb_smue(self, bb_select_mov_ue: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:BBSMue \n
		No command help available \n
			:param bb_select_mov_ue: No help available
		"""
		param = Conversions.decimal_value_to_str(bb_select_mov_ue)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:BBSMue {param}')

	def get_bb_ssue(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:BBSSue \n
		No command help available \n
			:return: bb_select_stat_ue: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:BBSSue?')
		return Conversions.str_to_int(response)

	def set_bb_ssue(self, bb_select_stat_ue: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:BBSSue \n
		No command help available \n
			:param bb_select_stat_ue: No help available
		"""
		param = Conversions.decimal_value_to_str(bb_select_stat_ue)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:BBSSue {param}')

	def get_bb_selector(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:BBSelector \n
		No command help available \n
			:return: bb_selector: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:BBSelector?')
		return Conversions.str_to_int(response)

	def set_bb_selector(self, bb_selector: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:BBSelector \n
		No command help available \n
			:param bb_selector: No help available
		"""
		param = Conversions.decimal_value_to_str(bb_selector)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:BBSelector {param}')

	# noinspection PyTypeChecker
	def get_conmue(self) -> enums.EutraTcwConnector:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:CONMue \n
		No command help available \n
			:return: connector_mov_ue: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:CONMue?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwConnector)

	def set_conmue(self, connector_mov_ue: enums.EutraTcwConnector) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:CONMue \n
		No command help available \n
			:param connector_mov_ue: No help available
		"""
		param = Conversions.enum_scalar_to_str(connector_mov_ue, enums.EutraTcwConnector)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:CONMue {param}')

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.EutraTcwConnector:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:CONNector \n
		No command help available \n
			:return: connector: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwConnector)

	def set_connector(self, connector: enums.EutraTcwConnector) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:CONNector \n
		No command help available \n
			:param connector: No help available
		"""
		param = Conversions.enum_scalar_to_str(connector, enums.EutraTcwConnector)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:CONNector {param}')

	# noinspection PyTypeChecker
	def get_consue(self) -> enums.EutraTcwConnector:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:CONSue \n
		No command help available \n
			:return: connector_stat_ue: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:CONSue?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwConnector)

	def set_consue(self, connector_stat_ue: enums.EutraTcwConnector) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:CONSue \n
		No command help available \n
			:param connector_stat_ue: No help available
		"""
		param = Conversions.enum_scalar_to_str(connector_stat_ue, enums.EutraTcwConnector)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:CONSue {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.EutraTcwrtfMode:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwrtfMode)

	def set_mode(self, mode: enums.EutraTcwrtfMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.EutraTcwrtfMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:MODE {param}')

	# noinspection PyTypeChecker
	def get_ser_rate(self) -> enums.EutraSerialRate:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:SERRate \n
		No command help available \n
			:return: serial_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:RTF:SERRate?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSerialRate)

	def set_ser_rate(self, serial_rate: enums.EutraSerialRate) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:RTF:SERRate \n
		No command help available \n
			:param serial_rate: No help available
		"""
		param = Conversions.enum_scalar_to_str(serial_rate, enums.EutraSerialRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:RTF:SERRate {param}')
