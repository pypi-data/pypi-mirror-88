from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Packet:
	"""Packet commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("packet", core, parent)

	def clone(self) -> 'Packet':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Packet(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Packet_.Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def infinite(self):
		"""infinite commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_infinite'):
			from .Packet_.Infinite import Infinite
			self._infinite = Infinite(self._core, self._base)
		return self._infinite

	@property
	def soffset(self):
		"""soffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_soffset'):
			from .Packet_.Soffset import Soffset
			self._soffset = Soffset(self._core, self._base)
		return self._soffset
