from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		
		self._base.multi_repcap_types = "Channel,CarrierComponent"

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def anPattern(self):
		"""anPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anPattern'):
			from .Cell_.AnPattern import AnPattern
			self._anPattern = AnPattern(self._core, self._base)
		return self._anPattern

	@property
	def group(self):
		"""group commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_group'):
			from .Cell_.Group import Group
			self._group = Group(self._core, self._base)
		return self._group

	@property
	def noGroups(self):
		"""noGroups commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noGroups'):
			from .Cell_.NoGroups import NoGroups
			self._noGroups = NoGroups(self._core, self._base)
		return self._noGroups
