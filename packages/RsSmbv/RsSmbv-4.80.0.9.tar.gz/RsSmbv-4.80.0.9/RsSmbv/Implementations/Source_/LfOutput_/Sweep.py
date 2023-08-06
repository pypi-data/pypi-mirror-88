from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sweep:
	"""Sweep commands group definition. 12 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sweep", core, parent)

	def clone(self) -> 'Sweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def frequency(self):
		"""frequency commands group. 3 Sub-classes, 7 commands."""
		if not hasattr(self, '_frequency'):
			from .Sweep_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency
