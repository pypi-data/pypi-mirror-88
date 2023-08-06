from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AckChannel:
	"""AckChannel commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ackChannel", core, parent)

	def clone(self) -> 'AckChannel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AckChannel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .AckChannel_.Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def gating(self):
		"""gating commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gating'):
			from .AckChannel_.Gating import Gating
			self._gating = Gating(self._core, self._base)
		return self._gating

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .AckChannel_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .AckChannel_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def values(self):
		"""values commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_values'):
			from .AckChannel_.Values import Values
			self._values = Values(self._core, self._base)
		return self._values
