from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cmode:
	"""Cmode commands group definition. 8 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cmode", core, parent)

	def clone(self) -> 'Cmode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cmode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def method(self):
		"""method commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_method'):
			from .Cmode_.Method import Method
			self._method = Method(self._core, self._base)
		return self._method

	@property
	def pattern(self):
		"""pattern commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pattern'):
			from .Cmode_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def poffset(self):
		"""poffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poffset'):
			from .Cmode_.Poffset import Poffset
			self._poffset = Poffset(self._core, self._base)
		return self._poffset

	@property
	def poMode(self):
		"""poMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poMode'):
			from .Cmode_.PoMode import PoMode
			self._poMode = PoMode(self._core, self._base)
		return self._poMode

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Cmode_.State import State
			self._state = State(self._core, self._base)
		return self._state
