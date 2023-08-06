from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Obscuration:
	"""Obscuration commands group definition. 6 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("obscuration", core, parent)

	def clone(self) -> 'Obscuration':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Obscuration(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def lmm(self):
		"""lmm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lmm'):
			from .Obscuration_.Lmm import Lmm
			self._lmm = Lmm(self._core, self._base)
		return self._lmm

	@property
	def rpl(self):
		"""rpl commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rpl'):
			from .Obscuration_.Rpl import Rpl
			self._rpl = Rpl(self._core, self._base)
		return self._rpl

	@property
	def vobs(self):
		"""vobs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_vobs'):
			from .Obscuration_.Vobs import Vobs
			self._vobs = Vobs(self._core, self._base)
		return self._vobs
