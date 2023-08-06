from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clock:
	"""Clock commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clock", core, parent)

	def clone(self) -> 'Clock':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Clock(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def af(self):
		"""af commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_af'):
			from .Clock_.Af import Af
			self._af = Af(self._core, self._base)
		return self._af

	@property
	def tgd(self):
		"""tgd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgd'):
			from .Clock_.Tgd import Tgd
			self._tgd = Tgd(self._core, self._base)
		return self._tgd

	@property
	def toc(self):
		"""toc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toc'):
			from .Clock_.Toc import Toc
			self._toc = Toc(self._core, self._base)
		return self._toc

	@property
	def wnoc(self):
		"""wnoc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wnoc'):
			from .Clock_.Wnoc import Wnoc
			self._wnoc = Wnoc(self._core, self._base)
		return self._wnoc
