from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Utc:
	"""Utc commands group definition. 8 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("utc", core, parent)

	def clone(self) -> 'Utc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Utc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aone(self):
		"""aone commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_aone'):
			from .Utc_.Aone import Aone
			self._aone = Aone(self._core, self._base)
		return self._aone

	@property
	def azero(self):
		"""azero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_azero'):
			from .Utc_.Azero import Azero
			self._azero = Azero(self._core, self._base)
		return self._azero

	@property
	def ioffset(self):
		"""ioffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ioffset'):
			from .Utc_.Ioffset import Ioffset
			self._ioffset = Ioffset(self._core, self._base)
		return self._ioffset

	@property
	def tot(self):
		"""tot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tot'):
			from .Utc_.Tot import Tot
			self._tot = Tot(self._core, self._base)
		return self._tot

	@property
	def wnot(self):
		"""wnot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wnot'):
			from .Utc_.Wnot import Wnot
			self._wnot = Wnot(self._core, self._base)
		return self._wnot
