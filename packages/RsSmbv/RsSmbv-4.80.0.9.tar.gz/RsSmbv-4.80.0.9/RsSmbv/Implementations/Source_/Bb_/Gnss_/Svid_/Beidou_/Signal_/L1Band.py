from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L1Band:
	"""L1Band commands group definition. 19 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("l1Band", core, parent)

	def clone(self) -> 'L1Band':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L1Band(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def b1C(self):
		"""b1C commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_b1C'):
			from .L1Band_.B1C import B1C
			self._b1C = B1C(self._core, self._base)
		return self._b1C

	@property
	def b1I(self):
		"""b1I commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_b1I'):
			from .L1Band_.B1I import B1I
			self._b1I = B1I(self._core, self._base)
		return self._b1I
