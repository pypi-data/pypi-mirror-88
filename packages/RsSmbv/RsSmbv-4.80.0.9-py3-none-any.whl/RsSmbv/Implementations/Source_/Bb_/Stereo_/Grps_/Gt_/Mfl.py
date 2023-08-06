from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mfl:
	"""Mfl commands group definition. 4 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mfl", core, parent)

	def clone(self) -> 'Mfl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mfl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Mfl_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def noEntries(self):
		"""noEntries commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noEntries'):
			from .Mfl_.NoEntries import NoEntries
			self._noEntries = NoEntries(self._core, self._base)
		return self._noEntries

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Mfl_.State import State
			self._state = State(self._core, self._base)
		return self._state
