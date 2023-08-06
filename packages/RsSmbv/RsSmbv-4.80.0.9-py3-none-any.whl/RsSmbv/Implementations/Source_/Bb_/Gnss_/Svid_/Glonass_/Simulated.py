from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Simulated:
	"""Simulated commands group definition. 15 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("simulated", core, parent)

	def clone(self) -> 'Simulated':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Simulated(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_clock'):
			from .Simulated_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def orbit(self):
		"""orbit commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_orbit'):
			from .Simulated_.Orbit import Orbit
			self._orbit = Orbit(self._core, self._base)
		return self._orbit
