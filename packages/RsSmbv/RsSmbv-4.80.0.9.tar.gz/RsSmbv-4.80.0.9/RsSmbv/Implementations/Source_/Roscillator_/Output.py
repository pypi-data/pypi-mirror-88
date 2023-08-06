from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	def clone(self) -> 'Output':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Output(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alternate(self):
		"""alternate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_alternate'):
			from .Output_.Alternate import Alternate
			self._alternate = Alternate(self._core, self._base)
		return self._alternate

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Output_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency
