from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def clone(self) -> 'File':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = File(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def constellation(self):
		"""constellation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_constellation'):
			from .File_.Constellation import Constellation
			self._constellation = Constellation(self._core, self._base)
		return self._constellation

	@property
	def nmessage(self):
		"""nmessage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nmessage'):
			from .File_.Nmessage import Nmessage
			self._nmessage = Nmessage(self._core, self._base)
		return self._nmessage
