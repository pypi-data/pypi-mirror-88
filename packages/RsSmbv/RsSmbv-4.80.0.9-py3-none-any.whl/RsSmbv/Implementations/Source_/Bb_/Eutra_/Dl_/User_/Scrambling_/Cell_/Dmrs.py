from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmrs:
	"""Dmrs commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmrs", core, parent)

	def clone(self) -> 'Dmrs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dmrs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def id1(self):
		"""id1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id1'):
			from .Dmrs_.Id1 import Id1
			self._id1 = Id1(self._core, self._base)
		return self._id1

	@property
	def id2(self):
		"""id2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id2'):
			from .Dmrs_.Id2 import Id2
			self._id2 = Id2(self._core, self._base)
		return self._id2

	@property
	def use(self):
		"""use commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_use'):
			from .Dmrs_.Use import Use
			self._use = Use(self._core, self._base)
		return self._use
