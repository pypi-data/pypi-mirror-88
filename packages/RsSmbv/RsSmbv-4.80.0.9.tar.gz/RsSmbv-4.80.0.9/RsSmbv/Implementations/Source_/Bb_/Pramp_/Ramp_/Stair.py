from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stair:
	"""Stair commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stair", core, parent)

	def clone(self) -> 'Stair':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Stair(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dwell(self):
		"""dwell commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dwell'):
			from .Stair_.Dwell import Dwell
			self._dwell = Dwell(self._core, self._base)
		return self._dwell

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Stair_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step
