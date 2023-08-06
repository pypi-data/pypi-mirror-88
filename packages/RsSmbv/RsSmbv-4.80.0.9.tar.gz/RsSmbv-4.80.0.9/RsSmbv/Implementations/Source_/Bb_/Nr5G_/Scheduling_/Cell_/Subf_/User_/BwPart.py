from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwPart:
	"""BwPart commands group definition. 345 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bwPart", core, parent)

	def clone(self) -> 'BwPart':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BwPart(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alloc(self):
		"""alloc commands group. 25 Sub-classes, 0 commands."""
		if not hasattr(self, '_alloc'):
			from .BwPart_.Alloc import Alloc
			self._alloc = Alloc(self._core, self._base)
		return self._alloc

	@property
	def nalloc(self):
		"""nalloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nalloc'):
			from .BwPart_.Nalloc import Nalloc
			self._nalloc = Nalloc(self._core, self._base)
		return self._nalloc

	@property
	def resulting(self):
		"""resulting commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_resulting'):
			from .BwPart_.Resulting import Resulting
			self._resulting = Resulting(self._core, self._base)
		return self._resulting
