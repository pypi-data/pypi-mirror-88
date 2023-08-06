from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rdata:
	"""Rdata commands group definition. 9 total commands, 9 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rdata", core, parent)

	def clone(self) -> 'Rdata':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rdata(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def hoppingParam(self):
		"""hoppingParam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hoppingParam'):
			from .Rdata_.HoppingParam import HoppingParam
			self._hoppingParam = HoppingParam(self._core, self._base)
		return self._hoppingParam

	@property
	def nsubbands(self):
		"""nsubbands commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsubbands'):
			from .Rdata_.Nsubbands import Nsubbands
			self._nsubbands = Nsubbands(self._core, self._base)
		return self._nsubbands

	@property
	def offsetInd(self):
		"""offsetInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offsetInd'):
			from .Rdata_.OffsetInd import OffsetInd
			self._offsetInd = OffsetInd(self._core, self._base)
		return self._offsetInd

	@property
	def prbNumber(self):
		"""prbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbNumber'):
			from .Rdata_.PrbNumber import PrbNumber
			self._prbNumber = PrbNumber(self._core, self._base)
		return self._prbNumber

	@property
	def prbStart(self):
		"""prbStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbStart'):
			from .Rdata_.PrbStart import PrbStart
			self._prbStart = PrbStart(self._core, self._base)
		return self._prbStart

	@property
	def prend(self):
		"""prend commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prend'):
			from .Rdata_.Prend import Prend
			self._prend = Prend(self._core, self._base)
		return self._prend

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .Rdata_.RbOffset import RbOffset
			self._rbOffset = RbOffset(self._core, self._base)
		return self._rbOffset

	@property
	def sfbmp(self):
		"""sfbmp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfbmp'):
			from .Rdata_.Sfbmp import Sfbmp
			self._sfbmp = Sfbmp(self._core, self._base)
		return self._sfbmp

	@property
	def trptSubset(self):
		"""trptSubset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trptSubset'):
			from .Rdata_.TrptSubset import TrptSubset
			self._trptSubset = TrptSubset(self._core, self._base)
		return self._trptSubset
