from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Antenna:
	"""Antenna commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("antenna", core, parent)

	def clone(self) -> 'Antenna':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Antenna(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Antenna_.Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def display(self):
		"""display commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Antenna_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	@property
	def v3D(self):
		"""v3D commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_v3D'):
			from .Antenna_.V3D import V3D
			self._v3D = V3D(self._core, self._base)
		return self._v3D
