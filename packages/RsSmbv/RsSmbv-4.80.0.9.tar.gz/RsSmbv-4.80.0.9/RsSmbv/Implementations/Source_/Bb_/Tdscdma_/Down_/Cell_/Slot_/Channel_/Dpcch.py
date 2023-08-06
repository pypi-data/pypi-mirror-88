from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpcch:
	"""Dpcch commands group definition. 9 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpcch", core, parent)

	def clone(self) -> 'Dpcch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dpcch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def sync(self):
		"""sync commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .Dpcch_.Sync import Sync
			self._sync = Sync(self._core, self._base)
		return self._sync

	@property
	def tfci(self):
		"""tfci commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tfci'):
			from .Dpcch_.Tfci import Tfci
			self._tfci = Tfci(self._core, self._base)
		return self._tfci

	@property
	def tpc(self):
		"""tpc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpc'):
			from .Dpcch_.Tpc import Tpc
			self._tpc = Tpc(self._core, self._base)
		return self._tpc
