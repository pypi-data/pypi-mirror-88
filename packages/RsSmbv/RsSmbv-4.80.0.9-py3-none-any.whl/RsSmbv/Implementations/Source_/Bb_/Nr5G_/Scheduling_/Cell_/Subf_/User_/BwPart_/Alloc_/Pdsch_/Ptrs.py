from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptrs:
	"""Ptrs commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptrs", core, parent)

	def clone(self) -> 'Ptrs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ptrs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def epre(self):
		"""epre commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_epre'):
			from .Ptrs_.Epre import Epre
			self._epre = Epre(self._core, self._base)
		return self._epre

	@property
	def frqDen(self):
		"""frqDen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frqDen'):
			from .Ptrs_.FrqDen import FrqDen
			self._frqDen = FrqDen(self._core, self._base)
		return self._frqDen

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Ptrs_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def reof(self):
		"""reof commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reof'):
			from .Ptrs_.Reof import Reof
			self._reof = Reof(self._core, self._base)
		return self._reof

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Ptrs_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tmDen(self):
		"""tmDen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmDen'):
			from .Ptrs_.TmDen import TmDen
			self._tmDen = TmDen(self._core, self._base)
		return self._tmDen
