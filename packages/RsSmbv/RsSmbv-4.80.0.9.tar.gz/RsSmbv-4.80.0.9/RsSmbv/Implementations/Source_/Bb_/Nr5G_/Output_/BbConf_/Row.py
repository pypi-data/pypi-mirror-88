from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Row:
	"""Row commands group definition. 6 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("row", core, parent)

	def clone(self) -> 'Row':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Row(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Row_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def pbrate(self):
		"""pbrate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pbrate'):
			from .Row_.Pbrate import Pbrate
			self._pbrate = Pbrate(self._core, self._base)
		return self._pbrate

	@property
	def peFile(self):
		"""peFile commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_peFile'):
			from .Row_.PeFile import PeFile
			self._peFile = PeFile(self._core, self._base)
		return self._peFile

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Row_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def variation(self):
		"""variation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_variation'):
			from .Row_.Variation import Variation
			self._variation = Variation(self._core, self._base)
		return self._variation
