from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 41 total commands, 10 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("niot", core, parent)

	def clone(self) -> 'Niot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Niot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def arb(self):
		"""arb commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arb'):
			from .Niot_.Arb import Arb
			self._arb = Arb(self._core, self._base)
		return self._arb

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Niot_.Dfreq import Dfreq
			self._dfreq = Dfreq(self._core, self._base)
		return self._dfreq

	@property
	def frc(self):
		"""frc commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_frc'):
			from .Niot_.Frc import Frc
			self._frc = Frc(self._core, self._base)
		return self._frc

	@property
	def ghDisable(self):
		"""ghDisable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ghDisable'):
			from .Niot_.GhDisable import GhDisable
			self._ghDisable = GhDisable(self._core, self._base)
		return self._ghDisable

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Niot_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def npssim(self):
		"""npssim commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npssim'):
			from .Niot_.Npssim import Npssim
			self._npssim = Npssim(self._core, self._base)
		return self._npssim

	@property
	def ntransmiss(self):
		"""ntransmiss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransmiss'):
			from .Niot_.Ntransmiss import Ntransmiss
			self._ntransmiss = Ntransmiss(self._core, self._base)
		return self._ntransmiss

	@property
	def rbIndex(self):
		"""rbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbIndex'):
			from .Niot_.RbIndex import RbIndex
			self._rbIndex = RbIndex(self._core, self._base)
		return self._rbIndex

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .Niot_.ScSpacing import ScSpacing
			self._scSpacing = ScSpacing(self._core, self._base)
		return self._scSpacing

	@property
	def trans(self):
		"""trans commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_trans'):
			from .Niot_.Trans import Trans
			self._trans = Trans(self._core, self._base)
		return self._trans
