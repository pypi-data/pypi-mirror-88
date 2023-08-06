from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Table:
	"""Table commands group definition. 10 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("table", core, parent)

	def clone(self) -> 'Table':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Table(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def amam(self):
		"""amam commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_amam'):
			from .Table_.Amam import Amam
			self._amam = Amam(self._core, self._base)
		return self._amam

	@property
	def amPm(self):
		"""amPm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_amPm'):
			from .Table_.AmPm import AmPm
			self._amPm = AmPm(self._core, self._base)
		return self._amPm

	@property
	def interp(self):
		"""interp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interp'):
			from .Table_.Interp import Interp
			self._interp = Interp(self._core, self._base)
		return self._interp

	@property
	def invert(self):
		"""invert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_invert'):
			from .Table_.Invert import Invert
			self._invert = Invert(self._core, self._base)
		return self._invert
