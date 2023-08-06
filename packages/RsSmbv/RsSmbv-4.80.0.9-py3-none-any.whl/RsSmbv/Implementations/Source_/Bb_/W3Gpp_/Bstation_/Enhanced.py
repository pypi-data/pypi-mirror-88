from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enhanced:
	"""Enhanced commands group definition. 46 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enhanced", core, parent)

	def clone(self) -> 'Enhanced':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Enhanced(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def channel(self):
		"""channel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Enhanced_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def pccpch(self):
		"""pccpch commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pccpch'):
			from .Enhanced_.Pccpch import Pccpch
			self._pccpch = Pccpch(self._core, self._base)
		return self._pccpch

	@property
	def pcpich(self):
		"""pcpich commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcpich'):
			from .Enhanced_.Pcpich import Pcpich
			self._pcpich = Pcpich(self._core, self._base)
		return self._pcpich
