from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pinon:
	"""Pinon commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pinon", core, parent)

	def clone(self) -> 'Pinon':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pinon(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pin(self):
		"""pin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pin'):
			from .Pinon_.Pin import Pin
			self._pin = Pin(self._core, self._base)
		return self._pin

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Pinon_.State import State
			self._state = State(self._core, self._base)
		return self._state
