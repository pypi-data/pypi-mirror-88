from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Harq:
	"""Harq commands group definition. 9 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("harq", core, parent)

	def clone(self) -> 'Harq':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Harq(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def simulation(self):
		"""simulation commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_simulation'):
			from .Harq_.Simulation import Simulation
			self._simulation = Simulation(self._core, self._base)
		return self._simulation
