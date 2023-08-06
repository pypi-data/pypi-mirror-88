from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Decimal:
	"""Decimal commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("decimal", core, parent)

	def clone(self) -> 'Decimal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Decimal(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pz(self):
		"""pz commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pz'):
			from .Decimal_.Pz import Pz
			self._pz = Pz(self._core, self._base)
		return self._pz

	@property
	def wgs(self):
		"""wgs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wgs'):
			from .Decimal_.Wgs import Wgs
			self._wgs = Wgs(self._core, self._base)
		return self._wgs
