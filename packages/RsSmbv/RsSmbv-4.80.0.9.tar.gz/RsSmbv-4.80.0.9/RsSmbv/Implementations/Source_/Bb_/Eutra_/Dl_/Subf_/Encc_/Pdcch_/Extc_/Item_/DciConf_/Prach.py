from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prach:
	"""Prach commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prach", core, parent)

	def clone(self) -> 'Prach':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Prach(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mindex(self):
		"""mindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mindex'):
			from .Prach_.Mindex import Mindex
			self._mindex = Mindex(self._core, self._base)
		return self._mindex

	@property
	def prIndex(self):
		"""prIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prIndex'):
			from .Prach_.PrIndex import PrIndex
			self._prIndex = PrIndex(self._core, self._base)
		return self._prIndex
