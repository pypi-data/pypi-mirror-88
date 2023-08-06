from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Location:
	"""Location commands group definition. 6 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("location", core, parent)

	def clone(self) -> 'Location':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Location(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def coordinates(self):
		"""coordinates commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_coordinates'):
			from .Location_.Coordinates import Coordinates
			self._coordinates = Coordinates(self._core, self._base)
		return self._coordinates

	@property
	def uradius(self):
		"""uradius commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uradius'):
			from .Location_.Uradius import Uradius
			self._uradius = Uradius(self._core, self._base)
		return self._uradius
