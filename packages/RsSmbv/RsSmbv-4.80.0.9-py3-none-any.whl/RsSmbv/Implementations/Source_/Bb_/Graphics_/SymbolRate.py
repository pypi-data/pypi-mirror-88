from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.TranRecSampFactMode:
		"""[SOURce<HW>]:BB:GRAPhics:SRATe:MODE \n
		Sets how the time resolution of the signal is determined. Maximum resolution corresponds to a diagram covering the entire
		signal bandwidth. The higher the resolution is, the shorter the length of the displayed signal segment will be for the
		specified recording depth. \n
			:return: mode: AUTO| FULL| USER
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GRAPhics:SRATe:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TranRecSampFactMode)

	def set_mode(self, mode: enums.TranRecSampFactMode) -> None:
		"""[SOURce<HW>]:BB:GRAPhics:SRATe:MODE \n
		Sets how the time resolution of the signal is determined. Maximum resolution corresponds to a diagram covering the entire
		signal bandwidth. The higher the resolution is, the shorter the length of the displayed signal segment will be for the
		specified recording depth. \n
			:param mode: AUTO| FULL| USER
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.TranRecSampFactMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GRAPhics:SRATe:MODE {param}')

	def get_user(self) -> float:
		"""[SOURce<HW>]:BB:GRAPhics:SRATe:USER \n
		(Enabled for BB:GRAPH:SRAT:MODE USER) Selects the signal bandwidth for the diagram. The setting range moves between the
		minimum and maximum bandwidth which is possible for the selected graphical signal display. The selection is made
		graphically by moving the pointer. \n
			:return: user: float Range: 0.01 to 100, Unit: PCT
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GRAPhics:SRATe:USER?')
		return Conversions.str_to_float(response)

	def set_user(self, user: float) -> None:
		"""[SOURce<HW>]:BB:GRAPhics:SRATe:USER \n
		(Enabled for BB:GRAPH:SRAT:MODE USER) Selects the signal bandwidth for the diagram. The setting range moves between the
		minimum and maximum bandwidth which is possible for the selected graphical signal display. The selection is made
		graphically by moving the pointer. \n
			:param user: float Range: 0.01 to 100, Unit: PCT
		"""
		param = Conversions.decimal_value_to_str(user)
		self._core.io.write(f'SOURce<HwInstance>:BB:GRAPhics:SRATe:USER {param}')
