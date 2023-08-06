from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Npdsch:
	"""Npdsch commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("npdsch", core, parent)

	def clone(self) -> 'Npdsch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Npdsch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def irep(self):
		"""irep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_irep'):
			from .Npdsch_.Irep import Irep
			self._irep = Irep(self._core, self._base)
		return self._irep

	@property
	def isf(self):
		"""isf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isf'):
			from .Npdsch_.Isf import Isf
			self._isf = Isf(self._core, self._base)
		return self._isf

	@property
	def nrep(self):
		"""nrep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrep'):
			from .Npdsch_.Nrep import Nrep
			self._nrep = Nrep(self._core, self._base)
		return self._nrep

	@property
	def nsf(self):
		"""nsf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsf'):
			from .Npdsch_.Nsf import Nsf
			self._nsf = Nsf(self._core, self._base)
		return self._nsf
