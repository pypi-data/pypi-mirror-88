from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L5Band:
	"""L5Band commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("l5Band", core, parent)

	def clone(self) -> 'L5Band':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L5Band(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def b2A(self):
		"""b2A commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_b2A'):
			from .L5Band_.B2A import B2A
			self._b2A = B2A(self._core, self._base)
		return self._b2A

	@property
	def b2I(self):
		"""b2I commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_b2I'):
			from .L5Band_.B2I import B2I
			self._b2I = B2I(self._core, self._base)
		return self._b2I
