from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attitude:
	"""Attitude commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("attitude", core, parent)

	def clone(self) -> 'Attitude':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Attitude(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pitch(self):
		"""pitch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pitch'):
			from .Attitude_.Pitch import Pitch
			self._pitch = Pitch(self._core, self._base)
		return self._pitch

	@property
	def roll(self):
		"""roll commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_roll'):
			from .Attitude_.Roll import Roll
			self._roll = Roll(self._core, self._base)
		return self._roll

	@property
	def spin(self):
		"""spin commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spin'):
			from .Attitude_.Spin import Spin
			self._spin = Spin(self._core, self._base)
		return self._spin

	@property
	def yaw(self):
		"""yaw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_yaw'):
			from .Attitude_.Yaw import Yaw
			self._yaw = Yaw(self._core, self._base)
		return self._yaw

	@property
	def behaviour(self):
		"""behaviour commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_behaviour'):
			from .Attitude_.Behaviour import Behaviour
			self._behaviour = Behaviour(self._core, self._base)
		return self._behaviour
