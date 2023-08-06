from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ul:
	"""Ul commands group definition. 121 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ul", core, parent)

	def clone(self) -> 'Ul':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ul(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bwp(self):
		"""bwp commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_bwp'):
			from .Ul_.Bwp import Bwp
			self._bwp = Bwp(self._core, self._base)
		return self._bwp

	@property
	def nbwParts(self):
		"""nbwParts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nbwParts'):
			from .Ul_.NbwParts import NbwParts
			self._nbwParts = NbwParts(self._core, self._base)
		return self._nbwParts
