from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cs:
	"""Cs commands group definition. 3 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cs", core, parent)

	def clone(self) -> 'Cs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ap(self):
		"""ap commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap'):
			from .Cs_.Ap import Ap
			self._ap = Ap(self._core, self._base)
		return self._ap

	@property
	def cell(self):
		"""cell commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Cs_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell
