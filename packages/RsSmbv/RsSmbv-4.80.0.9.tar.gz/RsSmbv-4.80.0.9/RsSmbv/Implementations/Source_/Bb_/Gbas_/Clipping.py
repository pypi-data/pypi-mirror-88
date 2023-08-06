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
		"""[SOURce<HW>]:BB:GBAS:CLIPping:LEVel \n
		Sets the limit for clipping. \n
			:return: level: integer Range: 1 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:CLIPping:LEVel?')
		return Conversions.str_to_int(response)

	def set_level(self, level: int) -> None:
		"""[SOURce<HW>]:BB:GBAS:CLIPping:LEVel \n
		Sets the limit for clipping. \n
			:param level: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:CLIPping:LEVel {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClipMode:
		"""[SOURce<HW>]:BB:GBAS:CLIPping:MODE \n
		Sets the clipping mode. \n
			:return: mode: VECTor| SCALar
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:CLIPping:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClipMode)

	def set_mode(self, mode: enums.ClipMode) -> None:
		"""[SOURce<HW>]:BB:GBAS:CLIPping:MODE \n
		Sets the clipping mode. \n
			:param mode: VECTor| SCALar
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClipMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:CLIPping:MODE {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:GBAS:CLIPping:STATe \n
		Enables/disable clipping. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:CLIPping:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:GBAS:CLIPping:STATe \n
		Enables/disable clipping. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:CLIPping:STATe {param}')
