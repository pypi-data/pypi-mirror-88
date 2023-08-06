from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Settings:
	"""Settings commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("settings", core, parent)

	def clone(self) -> 'Settings':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Settings(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def backup(self):
		"""backup commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_backup'):
			from .Settings_.Backup import Backup
			self._backup = Backup(self._core, self._base)
		return self._backup

	@property
	def restore(self):
		"""restore commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_restore'):
			from .Settings_.Restore import Restore
			self._restore = Restore(self._core, self._base)
		return self._restore
