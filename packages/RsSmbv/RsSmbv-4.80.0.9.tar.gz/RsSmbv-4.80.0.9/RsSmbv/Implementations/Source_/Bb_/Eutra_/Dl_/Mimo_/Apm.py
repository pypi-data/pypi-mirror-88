from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Apm:
	"""Apm commands group definition. 4 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apm", core, parent)

	def clone(self) -> 'Apm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Apm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cs(self):
		"""cs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cs'):
			from .Apm_.Cs import Cs
			self._cs = Cs(self._core, self._base)
		return self._cs

	# noinspection PyTypeChecker
	def get_map_coordinates(self) -> enums.CoordMapMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:APM:MAPCoordinates \n
		Switches between the cartesian and cylindrical coordinates representation. \n
			:return: type_py: CARTesian| CYLindrical
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MIMO:APM:MAPCoordinates?')
		return Conversions.str_to_scalar_enum(response, enums.CoordMapMode)

	def set_map_coordinates(self, type_py: enums.CoordMapMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:APM:MAPCoordinates \n
		Switches between the cartesian and cylindrical coordinates representation. \n
			:param type_py: CARTesian| CYLindrical
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.CoordMapMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MIMO:APM:MAPCoordinates {param}')
