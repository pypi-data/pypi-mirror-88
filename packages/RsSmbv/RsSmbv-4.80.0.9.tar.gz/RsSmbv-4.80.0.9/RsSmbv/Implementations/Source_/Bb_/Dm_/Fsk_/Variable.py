from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Variable:
	"""Variable commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("variable", core, parent)

	def clone(self) -> 'Variable':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Variable(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def symbol(self):
		"""symbol commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_symbol'):
			from .Variable_.Symbol import Symbol
			self._symbol = Symbol(self._core, self._base)
		return self._symbol

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFskModType:
		"""[SOURce<HW>]:BB:DM:FSK:VARiable:TYPE \n
		The command selects the modulation type for Variable FSK. \n
			:return: type_py: FSK4| FSK8| FSK16
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FSK:VARiable:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DmFskModType)

	def set_type_py(self, type_py: enums.DmFskModType) -> None:
		"""[SOURce<HW>]:BB:DM:FSK:VARiable:TYPE \n
		The command selects the modulation type for Variable FSK. \n
			:param type_py: FSK4| FSK8| FSK16
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFskModType)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FSK:VARiable:TYPE {param}')
