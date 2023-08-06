from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Permanent:
	"""Permanent commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("permanent", core, parent)

	def clone(self) -> 'Permanent':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Permanent(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def priority(self):
		"""priority commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_priority'):
			from .Permanent_.Priority import Priority
			self._priority = Priority(self._core, self._base)
		return self._priority

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Permanent_.State import State
			self._state = State(self._core, self._base)
		return self._state
