from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Waypoint:
	"""Waypoint commands group definition. 5 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("waypoint", core, parent)

	def clone(self) -> 'Waypoint':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Waypoint(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .Waypoint_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def predefined(self):
		"""predefined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_predefined'):
			from .Waypoint_.Predefined import Predefined
			self._predefined = Predefined(self._core, self._base)
		return self._predefined

	@property
	def user(self):
		"""user commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .Waypoint_.User import User
			self._user = User(self._core, self._base)
		return self._user
