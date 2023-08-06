from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DrcChannel:
	"""DrcChannel commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("drcChannel", core, parent)

	def clone(self) -> 'DrcChannel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DrcChannel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cover(self):
		"""cover commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cover'):
			from .DrcChannel_.Cover import Cover
			self._cover = Cover(self._core, self._base)
		return self._cover

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .DrcChannel_.Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def gating(self):
		"""gating commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gating'):
			from .DrcChannel_.Gating import Gating
			self._gating = Gating(self._core, self._base)
		return self._gating

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .DrcChannel_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .DrcChannel_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def values(self):
		"""values commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_values'):
			from .DrcChannel_.Values import Values
			self._values = Values(self._core, self._base)
		return self._values
