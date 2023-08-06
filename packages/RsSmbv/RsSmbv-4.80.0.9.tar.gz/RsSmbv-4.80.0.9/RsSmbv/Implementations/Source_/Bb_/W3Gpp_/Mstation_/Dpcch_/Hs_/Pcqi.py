from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pcqi:
	"""Pcqi commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pcqi", core, parent)

	def clone(self) -> 'Pcqi':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pcqi(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def repeat(self):
		"""repeat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repeat'):
			from .Pcqi_.Repeat import Repeat
			self._repeat = Repeat(self._core, self._base)
		return self._repeat

	@property
	def rows(self):
		"""rows commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rows'):
			from .Pcqi_.Rows import Rows
			self._rows = Rows(self._core, self._base)
		return self._rows
