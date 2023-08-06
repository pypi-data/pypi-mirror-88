from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Derror:
	"""Derror commands group definition. 5 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("derror", core, parent)

	def clone(self) -> 'Derror':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Derror(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bit(self):
		"""bit commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_bit'):
			from .Derror_.Bit import Bit
			self._bit = Bit(self._core, self._base)
		return self._bit

	@property
	def block(self):
		"""block commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_block'):
			from .Derror_.Block import Block
			self._block = Block(self._core, self._base)
		return self._block
