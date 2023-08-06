from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Location:
	"""Location commands group definition. 13 total commands, 6 Sub-groups, 0 group commands"""

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
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Location_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	@property
	def coordinates(self):
		"""coordinates commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_coordinates'):
			from .Location_.Coordinates import Coordinates
			self._coordinates = Coordinates(self._core, self._base)
		return self._coordinates

	@property
	def smovement(self):
		"""smovement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smovement'):
			from .Location_.Smovement import Smovement
			self._smovement = Smovement(self._core, self._base)
		return self._smovement

	@property
	def vehicle(self):
		"""vehicle commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_vehicle'):
			from .Location_.Vehicle import Vehicle
			self._vehicle = Vehicle(self._core, self._base)
		return self._vehicle

	@property
	def waypoints(self):
		"""waypoints commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_waypoints'):
			from .Location_.Waypoints import Waypoints
			self._waypoints = Waypoints(self._core, self._base)
		return self._waypoints

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Location_.Select import Select
			self._select = Select(self._core, self._base)
		return self._select
