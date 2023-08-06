from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Actable:
	"""Actable commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("actable", core, parent)

	def clone(self) -> 'Actable':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Actable(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def channel(self):
		"""channel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Actable_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def set(self):
		"""set commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_set'):
			from .Actable_.Set import Set
			self._set = Set(self._core, self._base)
		return self._set
