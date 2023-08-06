from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Amplifier:
	"""Amplifier commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("amplifier", core, parent)

	def clone(self) -> 'Amplifier':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Amplifier(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def stage(self):
		"""stage commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_stage'):
			from .Amplifier_.Stage import Stage
			self._stage = Stage(self._core, self._base)
		return self._stage
