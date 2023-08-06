from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Update:
	"""Update commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("update", core, parent)

	def clone(self) -> 'Update':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Update(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Update_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	def set_value(self, action_sel: enums.CalDataUpdate) -> None:
		"""CALibration<HW>:DATA:UPDate \n
		No command help available \n
			:param action_sel: No help available
		"""
		param = Conversions.enum_scalar_to_str(action_sel, enums.CalDataUpdate)
		self._core.io.write(f'CALibration<HwInstance>:DATA:UPDate {param}')
