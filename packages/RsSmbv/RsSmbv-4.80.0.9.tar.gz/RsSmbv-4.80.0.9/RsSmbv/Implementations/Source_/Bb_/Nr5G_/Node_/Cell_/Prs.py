from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prs:
	"""Prs commands group definition. 21 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prs", core, parent)

	def clone(self) -> 'Prs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Prs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def nrSets(self):
		"""nrSets commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrSets'):
			from .Prs_.NrSets import NrSets
			self._nrSets = NrSets(self._core, self._base)
		return self._nrSets

	@property
	def rset(self):
		"""rset commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_rset'):
			from .Prs_.Rset import Rset
			self._rset = Rset(self._core, self._base)
		return self._rset

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .Prs_.ScSpacing import ScSpacing
			self._scSpacing = ScSpacing(self._core, self._base)
		return self._scSpacing

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Prs_.State import State
			self._state = State(self._core, self._base)
		return self._state
