from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CarMapping:
	"""CarMapping commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("carMapping", core, parent)

	def clone(self) -> 'CarMapping':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CarMapping(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ap4000(self):
		"""ap4000 commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap4000'):
			from .CarMapping_.Ap4000 import Ap4000
			self._ap4000 = Ap4000(self._core, self._base)
		return self._ap4000

	@property
	def cell(self):
		"""cell commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .CarMapping_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell
