from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clipping:
	"""Clipping commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clipping", core, parent)

	def get_level(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:CLIPping:LEVel \n
		Sets the limit for level clipping. \n
			:return: level: integer Range: 1 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:CLIPping:LEVel?')
		return Conversions.str_to_int(response)

	def set_level(self, level: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:CLIPping:LEVel \n
		Sets the limit for level clipping. \n
			:param level: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:CLIPping:LEVel {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClipMode:
		"""[SOURce<HW>]:BB:EUTRa:CLIPping:MODE \n
		Sets the method for level clipping. \n
			:return: mode: VECTor| SCALar VECTor The reference level is the amplitude | i+jq |. SCALar The reference level is the absolute maximum of the I and Q values.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:CLIPping:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClipMode)

	def set_mode(self, mode: enums.ClipMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:CLIPping:MODE \n
		Sets the method for level clipping. \n
			:param mode: VECTor| SCALar VECTor The reference level is the amplitude | i+jq |. SCALar The reference level is the absolute maximum of the I and Q values.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClipMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:CLIPping:MODE {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:CLIPping:STATe \n
		Activates level clipping (Clipping) . The value is defined with the command [SOURce:]BB:EUTRa:CLIPping:LEVel, the mode of
		calculation with the command [SOURce:]BB:EUTRa:CLIPping:MODE. \n
			:return: state: ON| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:CLIPping:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:CLIPping:STATe \n
		Activates level clipping (Clipping) . The value is defined with the command [SOURce:]BB:EUTRa:CLIPping:LEVel, the mode of
		calculation with the command [SOURce:]BB:EUTRa:CLIPping:MODE. \n
			:param state: ON| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:CLIPping:STATe {param}')
