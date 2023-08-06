from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enhanced:
	"""Enhanced commands group definition. 39 total commands, 3 Sub-groups, 0 group commands"""

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
	def dpdch(self):
		"""dpdch commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_dpdch'):
			from .Enhanced_.Dpdch import Dpdch
			self._dpdch = Dpdch(self._core, self._base)
		return self._dpdch

	@property
	def pcpch(self):
		"""pcpch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcpch'):
			from .Enhanced_.Pcpch import Pcpch
			self._pcpch = Pcpch(self._core, self._base)
		return self._pcpch

	@property
	def prach(self):
		"""prach commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_prach'):
			from .Enhanced_.Prach import Prach
			self._prach = Prach(self._core, self._base)
		return self._prach
