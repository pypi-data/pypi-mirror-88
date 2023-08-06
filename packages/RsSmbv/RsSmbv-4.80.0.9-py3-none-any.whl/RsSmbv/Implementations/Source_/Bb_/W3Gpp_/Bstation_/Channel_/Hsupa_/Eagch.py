from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eagch:
	"""Eagch commands group definition. 6 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eagch", core, parent)

	def clone(self) -> 'Eagch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Eagch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ifCoding(self):
		"""ifCoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ifCoding'):
			from .Eagch_.IfCoding import IfCoding
			self._ifCoding = IfCoding(self._core, self._base)
		return self._ifCoding

	@property
	def tti(self):
		"""tti commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tti'):
			from .Eagch_.Tti import Tti
			self._tti = Tti(self._core, self._base)
		return self._tti

	@property
	def ttiCount(self):
		"""ttiCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiCount'):
			from .Eagch_.TtiCount import TtiCount
			self._ttiCount = TtiCount(self._core, self._base)
		return self._ttiCount

	@property
	def ttiedch(self):
		"""ttiedch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiedch'):
			from .Eagch_.Ttiedch import Ttiedch
			self._ttiedch = Ttiedch(self._core, self._base)
		return self._ttiedch
