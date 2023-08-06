from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Emtc:
	"""Emtc commands group definition. 36 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("emtc", core, parent)

	def clone(self) -> 'Emtc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Emtc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def arb(self):
		"""arb commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arb'):
			from .Emtc_.Arb import Arb
			self._arb = Arb(self._core, self._base)
		return self._arb

	@property
	def ceLevel(self):
		"""ceLevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ceLevel'):
			from .Emtc_.CeLevel import CeLevel
			self._ceLevel = CeLevel(self._core, self._base)
		return self._ceLevel

	@property
	def hopp(self):
		"""hopp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hopp'):
			from .Emtc_.Hopp import Hopp
			self._hopp = Hopp(self._core, self._base)
		return self._hopp

	@property
	def ntransmiss(self):
		"""ntransmiss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransmiss'):
			from .Emtc_.Ntransmiss import Ntransmiss
			self._ntransmiss = Ntransmiss(self._core, self._base)
		return self._ntransmiss

	@property
	def trans(self):
		"""trans commands group. 23 Sub-classes, 0 commands."""
		if not hasattr(self, '_trans'):
			from .Emtc_.Trans import Trans
			self._trans = Trans(self._core, self._base)
		return self._trans
