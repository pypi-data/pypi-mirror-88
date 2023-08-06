from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Poffset:
	"""Poffset commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poffset", core, parent)

	def clone(self) -> 'Poffset':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Poffset(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pilot(self):
		"""pilot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pilot'):
			from .Poffset_.Pilot import Pilot
			self._pilot = Pilot(self._core, self._base)
		return self._pilot

	@property
	def tfci(self):
		"""tfci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfci'):
			from .Poffset_.Tfci import Tfci
			self._tfci = Tfci(self._core, self._base)
		return self._tfci

	@property
	def tpc(self):
		"""tpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpc'):
			from .Poffset_.Tpc import Tpc
			self._tpc = Tpc(self._core, self._base)
		return self._tpc
