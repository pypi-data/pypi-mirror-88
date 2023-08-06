from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bit:
	"""Bit commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bit", core, parent)

	def clone(self) -> 'Bit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def layer(self):
		"""layer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_layer'):
			from .Bit_.Layer import Layer
			self._layer = Layer(self._core, self._base)
		return self._layer

	@property
	def rate(self):
		"""rate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .Bit_.Rate import Rate
			self._rate = Rate(self._core, self._base)
		return self._rate

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Bit_.State import State
			self._state = State(self._core, self._base)
		return self._state
