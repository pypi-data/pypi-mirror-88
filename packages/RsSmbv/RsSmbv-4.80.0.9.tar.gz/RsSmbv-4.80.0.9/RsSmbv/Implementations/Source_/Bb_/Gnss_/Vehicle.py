from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vehicle:
	"""Vehicle commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vehicle", core, parent)

	def clone(self) -> 'Vehicle':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Vehicle(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_catalog'):
			from .Vehicle_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	# noinspection PyTypeChecker
	def get_count(self) -> enums.Count:
		"""[SOURce<HW>]:BB:GNSS:VEHicle:COUNt \n
		No command help available \n
			:return: number_of_vehicle: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:VEHicle:COUNt?')
		return Conversions.str_to_scalar_enum(response, enums.Count)

	def set_count(self, number_of_vehicle: enums.Count) -> None:
		"""[SOURce<HW>]:BB:GNSS:VEHicle:COUNt \n
		No command help available \n
			:param number_of_vehicle: No help available
		"""
		param = Conversions.enum_scalar_to_str(number_of_vehicle, enums.Count)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:VEHicle:COUNt {param}')
