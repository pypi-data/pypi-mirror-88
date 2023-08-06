from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enh:
	"""Enh commands group definition. 88 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enh", core, parent)

	def clone(self) -> 'Enh':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Enh(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dch(self):
		"""dch commands group. 17 Sub-classes, 0 commands."""
		if not hasattr(self, '_dch'):
			from .Enh_.Dch import Dch
			self._dch = Dch(self._core, self._base)
		return self._dch
