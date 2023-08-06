from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptyta:
	"""Ptyta commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptyta", core, parent)

	def clone(self) -> 'Ptyta':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ptyta(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pty(self):
		"""pty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pty'):
			from .Ptyta_.Pty import Pty
			self._pty = Pty(self._core, self._base)
		return self._pty

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Ptyta_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def ta(self):
		"""ta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ta'):
			from .Ptyta_.Ta import Ta
			self._ta = Ta(self._core, self._base)
		return self._ta
