from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


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
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Output_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def pep(self):
		"""pep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pep'):
			from .Output_.Pep import Pep
			self._pep = Pep(self._core, self._base)
		return self._pep
