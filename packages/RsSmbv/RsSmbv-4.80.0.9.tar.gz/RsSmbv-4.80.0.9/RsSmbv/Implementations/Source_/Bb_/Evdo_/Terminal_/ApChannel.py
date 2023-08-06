from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApChannel:
	"""ApChannel commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apChannel", core, parent)

	def clone(self) -> 'ApChannel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApChannel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .ApChannel_.Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def payload(self):
		"""payload commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_payload'):
			from .ApChannel_.Payload import Payload
			self._payload = Payload(self._core, self._base)
		return self._payload

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .ApChannel_.State import State
			self._state = State(self._core, self._base)
		return self._state
