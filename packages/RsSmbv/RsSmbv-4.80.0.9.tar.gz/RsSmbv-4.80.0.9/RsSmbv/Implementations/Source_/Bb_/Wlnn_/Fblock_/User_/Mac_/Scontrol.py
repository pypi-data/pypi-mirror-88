from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scontrol:
	"""Scontrol commands group definition. 5 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scontrol", core, parent)

	def clone(self) -> 'Scontrol':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scontrol(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fragment(self):
		"""fragment commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fragment'):
			from .Scontrol_.Fragment import Fragment
			self._fragment = Fragment(self._core, self._base)
		return self._fragment

	@property
	def sequence(self):
		"""sequence commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequence'):
			from .Scontrol_.Sequence import Sequence
			self._sequence = Sequence(self._core, self._base)
		return self._sequence

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Scontrol_.State import State
			self._state = State(self._core, self._base)
		return self._state
