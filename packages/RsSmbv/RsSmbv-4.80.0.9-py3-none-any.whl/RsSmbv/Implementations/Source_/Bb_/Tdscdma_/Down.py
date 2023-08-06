from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Down:
	"""Down commands group definition. 147 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("down", core, parent)

	def clone(self) -> 'Down':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Down(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cell(self):
		"""cell commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Down_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def pparameter(self):
		"""pparameter commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pparameter'):
			from .Down_.Pparameter import Pparameter
			self._pparameter = Pparameter(self._core, self._base)
		return self._pparameter
