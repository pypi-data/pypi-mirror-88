from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lion:
	"""Lion commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lion", core, parent)

	def clone(self) -> 'Lion':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Lion(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def eg(self):
		"""eg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eg'):
			from .Lion_.Eg import Eg
			self._eg = Eg(self._core, self._base)
		return self._eg

	@property
	def ils(self):
		"""ils commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ils'):
			from .Lion_.Ils import Ils
			self._ils = Ils(self._core, self._base)
		return self._ils

	@property
	def la(self):
		"""la commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_la'):
			from .Lion_.La import La
			self._la = La(self._core, self._base)
		return self._la

	@property
	def lsn(self):
		"""lsn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lsn'):
			from .Lion_.Lsn import Lsn
			self._lsn = Lsn(self._core, self._base)
		return self._lsn

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Lion_.State import State
			self._state = State(self._core, self._base)
		return self._state
