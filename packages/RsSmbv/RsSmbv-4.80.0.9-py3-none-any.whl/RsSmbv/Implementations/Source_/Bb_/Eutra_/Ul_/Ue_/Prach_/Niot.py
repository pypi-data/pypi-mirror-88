from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

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
	def mod(self):
		"""mod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mod'):
			from .Niot_.Mod import Mod
			self._mod = Mod(self._core, self._base)
		return self._mod

	@property
	def prAttempts(self):
		"""prAttempts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prAttempts'):
			from .Niot_.PrAttempts import PrAttempts
			self._prAttempts = PrAttempts(self._core, self._base)
		return self._prAttempts

	@property
	def rbid(self):
		"""rbid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbid'):
			from .Niot_.Rbid import Rbid
			self._rbid = Rbid(self._core, self._base)
		return self._rbid
