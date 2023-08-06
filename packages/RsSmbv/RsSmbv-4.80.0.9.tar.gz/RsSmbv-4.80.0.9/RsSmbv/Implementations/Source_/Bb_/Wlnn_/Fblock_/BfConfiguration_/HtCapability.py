from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HtCapability:
	"""HtCapability commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("htCapability", core, parent)

	def clone(self) -> 'HtCapability':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HtCapability(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def gfield(self):
		"""gfield commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gfield'):
			from .HtCapability_.Gfield import Gfield
			self._gfield = Gfield(self._core, self._base)
		return self._gfield

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .HtCapability_.State import State
			self._state = State(self._core, self._base)
		return self._state
