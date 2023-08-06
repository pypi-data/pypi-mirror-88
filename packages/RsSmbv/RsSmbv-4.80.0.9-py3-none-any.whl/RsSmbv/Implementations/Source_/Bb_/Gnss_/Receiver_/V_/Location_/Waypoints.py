from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Waypoints:
	"""Waypoints commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("waypoints", core, parent)

	def clone(self) -> 'Waypoints':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Waypoints(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Waypoints_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .Waypoints_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def roMode(self):
		"""roMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_roMode'):
			from .Waypoints_.RoMode import RoMode
			self._roMode = RoMode(self._core, self._base)
		return self._roMode
