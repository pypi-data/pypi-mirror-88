from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dl:
	"""Dl commands group definition. 30 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dl", core, parent)

	def clone(self) -> 'Dl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def afSeq(self):
		"""afSeq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_afSeq'):
			from .Dl_.AfSeq import AfSeq
			self._afSeq = AfSeq(self._core, self._base)
		return self._afSeq

	@property
	def cell(self):
		"""cell commands group. 12 Sub-classes, 2 commands."""
		if not hasattr(self, '_cell'):
			from .Dl_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def indi(self):
		"""indi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_indi'):
			from .Dl_.Indi import Indi
			self._indi = Indi(self._core, self._base)
		return self._indi

	@property
	def nhids(self):
		"""nhids commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nhids'):
			from .Dl_.Nhids import Nhids
			self._nhids = Nhids(self._core, self._base)
		return self._nhids

	@property
	def nhtrans(self):
		"""nhtrans commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nhtrans'):
			from .Dl_.Nhtrans import Nhtrans
			self._nhtrans = Nhtrans(self._core, self._base)
		return self._nhtrans

	@property
	def skProcess(self):
		"""skProcess commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_skProcess'):
			from .Dl_.SkProcess import SkProcess
			self._skProcess = SkProcess(self._core, self._base)
		return self._skProcess
