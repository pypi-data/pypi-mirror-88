from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pucch:
	"""Pucch commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

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
	def f1Naport(self):
		"""f1Naport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f1Naport'):
			from .Pucch_.F1Naport import F1Naport
			self._f1Naport = F1Naport(self._core, self._base)
		return self._f1Naport

	@property
	def f2Naport(self):
		"""f2Naport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f2Naport'):
			from .Pucch_.F2Naport import F2Naport
			self._f2Naport = F2Naport(self._core, self._base)
		return self._f2Naport

	@property
	def f3Naport(self):
		"""f3Naport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f3Naport'):
			from .Pucch_.F3Naport import F3Naport
			self._f3Naport = F3Naport(self._core, self._base)
		return self._f3Naport

	@property
	def f4Naport(self):
		"""f4Naport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f4Naport'):
			from .Pucch_.F4Naport import F4Naport
			self._f4Naport = F4Naport(self._core, self._base)
		return self._f4Naport

	@property
	def f5Naport(self):
		"""f5Naport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f5Naport'):
			from .Pucch_.F5Naport import F5Naport
			self._f5Naport = F5Naport(self._core, self._base)
		return self._f5Naport
