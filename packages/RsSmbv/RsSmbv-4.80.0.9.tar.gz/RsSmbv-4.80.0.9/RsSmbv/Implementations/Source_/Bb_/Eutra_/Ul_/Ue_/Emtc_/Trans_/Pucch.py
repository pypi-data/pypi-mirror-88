from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pucch:
	"""Pucch commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pucch", core, parent)

	def clone(self) -> 'Pucch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pucch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cqi(self):
		"""cqi commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cqi'):
			from .Pucch_.Cqi import Cqi
			self._cqi = Cqi(self._core, self._base)
		return self._cqi

	@property
	def harq(self):
		"""harq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Pucch_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq
