from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Refsig:
	"""Refsig commands group definition. 20 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("refsig", core, parent)

	def clone(self) -> 'Refsig':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Refsig(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def anstx(self):
		"""anstx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anstx'):
			from .Refsig_.Anstx import Anstx
			self._anstx = Anstx(self._core, self._base)
		return self._anstx

	@property
	def drs(self):
		"""drs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_drs'):
			from .Refsig_.Drs import Drs
			self._drs = Drs(self._core, self._base)
		return self._drs

	@property
	def srs(self):
		"""srs commands group. 16 Sub-classes, 0 commands."""
		if not hasattr(self, '_srs'):
			from .Refsig_.Srs import Srs
			self._srs = Srs(self._core, self._base)
		return self._srs
