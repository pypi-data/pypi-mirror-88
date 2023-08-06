from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 4 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def copy(self):
		"""copy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_copy'):
			from .Power_.Copy import Copy
			self._copy = Copy(self._core, self._base)
		return self._copy

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Power_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def ploss(self):
		"""ploss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ploss'):
			from .Power_.Ploss import Ploss
			self._ploss = Ploss(self._core, self._base)
		return self._ploss
