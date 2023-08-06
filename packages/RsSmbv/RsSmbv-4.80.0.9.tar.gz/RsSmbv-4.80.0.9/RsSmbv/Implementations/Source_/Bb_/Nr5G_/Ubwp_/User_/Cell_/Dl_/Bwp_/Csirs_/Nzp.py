from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nzp:
	"""Nzp commands group definition. 19 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nzp", core, parent)

	def clone(self) -> 'Nzp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nzp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def set(self):
		"""set commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_set'):
			from .Nzp_.Set import Set
			self._set = Set(self._core, self._base)
		return self._set

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Nzp_.State import State
			self._state = State(self._core, self._base)
		return self._state
