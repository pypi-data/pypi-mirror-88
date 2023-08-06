from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Afon:
	"""Afon commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("afon", core, parent)

	def clone(self) -> 'Afon':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Afon(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Afon_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def noEntries(self):
		"""noEntries commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noEntries'):
			from .Afon_.NoEntries import NoEntries
			self._noEntries = NoEntries(self._core, self._base)
		return self._noEntries

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Afon_.State import State
			self._state = State(self._core, self._base)
		return self._state
