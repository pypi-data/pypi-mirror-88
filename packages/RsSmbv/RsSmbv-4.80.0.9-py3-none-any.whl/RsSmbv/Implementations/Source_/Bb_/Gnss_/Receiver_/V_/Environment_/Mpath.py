from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mpath:
	"""Mpath commands group definition. 5 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mpath", core, parent)

	def clone(self) -> 'Mpath':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mpath(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def copy(self):
		"""copy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_copy'):
			from .Mpath_.Copy import Copy
			self._copy = Copy(self._core, self._base)
		return self._copy

	@property
	def svid(self):
		"""svid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_svid'):
			from .Mpath_.Svid import Svid
			self._svid = Svid(self._core, self._base)
		return self._svid

	@property
	def system(self):
		"""system commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_system'):
			from .Mpath_.System import System
			self._system = System(self._core, self._base)
		return self._system
