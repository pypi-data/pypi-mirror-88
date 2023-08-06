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
		"""[SOURce<HW>]:BB:TDSCdma:CLIPping:LEVel \n
		Sets the limit for clipping. This value indicates at what point the signal is clipped. It is specified as a percentage,
		relative to the highest level. 100% indicates that clipping does not take place. \n
			:return: level: integer Range: 1 to 100, Unit: PCT
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:CLIPping:LEVel?')
		return Conversions.str_to_int(response)

	def set_level(self, level: int) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:CLIPping:LEVel \n
		Sets the limit for clipping. This value indicates at what point the signal is clipped. It is specified as a percentage,
		relative to the highest level. 100% indicates that clipping does not take place. \n
			:param level: integer Range: 1 to 100, Unit: PCT
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:CLIPping:LEVel {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClipMode:
		"""[SOURce<HW>]:BB:TDSCdma:CLIPping:MODE \n
		Sets the method for level clipping. \n
			:return: mode: VECTor| SCALar VECTor The reference level is the amplitude. SCALar The reference level is the absolute maximum of the I and Q values.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:CLIPping:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClipMode)

	def set_mode(self, mode: enums.ClipMode) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:CLIPping:MODE \n
		Sets the method for level clipping. \n
			:param mode: VECTor| SCALar VECTor The reference level is the amplitude. SCALar The reference level is the absolute maximum of the I and Q values.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClipMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:CLIPping:MODE {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:TDSCdma:CLIPping:STATe \n
		Activates level clipping \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:CLIPping:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:CLIPping:STATe \n
		Activates level clipping \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:CLIPping:STATe {param}')
