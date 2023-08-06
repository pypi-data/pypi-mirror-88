from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccorrection:
	"""Ccorrection commands group definition. 6 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccorrection", core, parent)

	def clone(self) -> 'Ccorrection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ccorrection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def af(self):
		"""af commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_af'):
			from .Ccorrection_.Af import Af
			self._af = Af(self._core, self._base)
		return self._af

	@property
	def tgd(self):
		"""tgd commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgd'):
			from .Ccorrection_.Tgd import Tgd
			self._tgd = Tgd(self._core, self._base)
		return self._tgd

	@property
	def toc(self):
		"""toc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_toc'):
			from .Ccorrection_.Toc import Toc
			self._toc = Toc(self._core, self._base)
		return self._toc
