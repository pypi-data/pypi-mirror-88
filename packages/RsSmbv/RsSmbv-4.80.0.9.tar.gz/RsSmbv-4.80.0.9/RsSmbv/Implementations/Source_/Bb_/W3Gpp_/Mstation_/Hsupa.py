from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hsupa:
	"""Hsupa commands group definition. 60 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hsupa", core, parent)

	def clone(self) -> 'Hsupa':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hsupa(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def channel(self):
		"""channel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Hsupa_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def dpcch(self):
		"""dpcch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpcch'):
			from .Hsupa_.Dpcch import Dpcch
			self._dpcch = Dpcch(self._core, self._base)
		return self._dpcch

	@property
	def dpdch(self):
		"""dpdch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpdch'):
			from .Hsupa_.Dpdch import Dpdch
			self._dpdch = Dpdch(self._core, self._base)
		return self._dpdch

	@property
	def edch(self):
		"""edch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_edch'):
			from .Hsupa_.Edch import Edch
			self._edch = Edch(self._core, self._base)
		return self._edch
