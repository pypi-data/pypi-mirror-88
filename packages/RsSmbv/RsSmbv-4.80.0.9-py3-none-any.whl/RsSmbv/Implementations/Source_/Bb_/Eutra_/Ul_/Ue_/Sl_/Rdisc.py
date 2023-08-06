from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rdisc:
	"""Rdisc commands group definition. 13 total commands, 13 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rdisc", core, parent)

	def clone(self) -> 'Rdisc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rdisc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cperiod(self):
		"""cperiod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cperiod'):
			from .Rdisc_.Cperiod import Cperiod
			self._cperiod = Cperiod(self._core, self._base)
		return self._cperiod

	@property
	def n1Pdsch(self):
		"""n1Pdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n1Pdsch'):
			from .Rdisc_.N1Pdsch import N1Pdsch
			self._n1Pdsch = N1Pdsch(self._core, self._base)
		return self._n1Pdsch

	@property
	def n2Pdsch(self):
		"""n2Pdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Pdsch'):
			from .Rdisc_.N2Pdsch import N2Pdsch
			self._n2Pdsch = N2Pdsch(self._core, self._base)
		return self._n2Pdsch

	@property
	def n3Pdsch(self):
		"""n3Pdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n3Pdsch'):
			from .Rdisc_.N3Pdsch import N3Pdsch
			self._n3Pdsch = N3Pdsch(self._core, self._base)
		return self._n3Pdsch

	@property
	def nrepetitions(self):
		"""nrepetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrepetitions'):
			from .Rdisc_.Nrepetitions import Nrepetitions
			self._nrepetitions = Nrepetitions(self._core, self._base)
		return self._nrepetitions

	@property
	def nretrans(self):
		"""nretrans commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nretrans'):
			from .Rdisc_.Nretrans import Nretrans
			self._nretrans = Nretrans(self._core, self._base)
		return self._nretrans

	@property
	def offsetInd(self):
		"""offsetInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offsetInd'):
			from .Rdisc_.OffsetInd import OffsetInd
			self._offsetInd = OffsetInd(self._core, self._base)
		return self._offsetInd

	@property
	def prbNumber(self):
		"""prbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbNumber'):
			from .Rdisc_.PrbNumber import PrbNumber
			self._prbNumber = PrbNumber(self._core, self._base)
		return self._prbNumber

	@property
	def prbStart(self):
		"""prbStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbStart'):
			from .Rdisc_.PrbStart import PrbStart
			self._prbStart = PrbStart(self._core, self._base)
		return self._prbStart

	@property
	def prend(self):
		"""prend commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prend'):
			from .Rdisc_.Prend import Prend
			self._prend = Prend(self._core, self._base)
		return self._prend

	@property
	def prIndex(self):
		"""prIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prIndex'):
			from .Rdisc_.PrIndex import PrIndex
			self._prIndex = PrIndex(self._core, self._base)
		return self._prIndex

	@property
	def sfbmp(self):
		"""sfbmp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfbmp'):
			from .Rdisc_.Sfbmp import Sfbmp
			self._sfbmp = Sfbmp(self._core, self._base)
		return self._sfbmp

	@property
	def sfIndex(self):
		"""sfIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfIndex'):
			from .Rdisc_.SfIndex import SfIndex
			self._sfIndex = SfIndex(self._core, self._base)
		return self._sfIndex
