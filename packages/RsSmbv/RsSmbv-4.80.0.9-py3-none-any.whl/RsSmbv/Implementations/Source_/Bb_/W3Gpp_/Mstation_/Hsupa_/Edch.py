from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Edch:
	"""Edch commands group definition. 5 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("edch", core, parent)

	def clone(self) -> 'Edch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Edch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def repeat(self):
		"""repeat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repeat'):
			from .Edch_.Repeat import Repeat
			self._repeat = Repeat(self._core, self._base)
		return self._repeat

	@property
	def row(self):
		"""row commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Edch_.Row import Row
			self._row = Row(self._core, self._base)
		return self._row

	@property
	def rowcount(self):
		"""rowcount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rowcount'):
			from .Edch_.Rowcount import Rowcount
			self._rowcount = Rowcount(self._core, self._base)
		return self._rowcount

	@property
	def ttiedch(self):
		"""ttiedch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiedch'):
			from .Edch_.Ttiedch import Ttiedch
			self._ttiedch = Ttiedch(self._core, self._base)
		return self._ttiedch
