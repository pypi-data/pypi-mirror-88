from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bwp:
	"""Bwp commands group definition. 129 total commands, 18 Sub-groups, 0 group commands
	Repeated Capability: NumSuffix, default value after init: NumSuffix.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bwp", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_numSuffix_get', 'repcap_numSuffix_set', repcap.NumSuffix.Nr0)

	def clone(self) -> 'Bwp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bwp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_numSuffix_set(self, enum_value: repcap.NumSuffix) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to NumSuffix.Default
		Default value after init: NumSuffix.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_numSuffix_get(self) -> repcap.NumSuffix:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def ciLength(self):
		"""ciLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ciLength'):
			from .Bwp_.CiLength import CiLength
			self._ciLength = CiLength(self._core, self._base)
		return self._ciLength

	@property
	def csi(self):
		"""csi commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_csi'):
			from .Bwp_.Csi import Csi
			self._csi = Csi(self._core, self._base)
		return self._csi

	@property
	def csirs(self):
		"""csirs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_csirs'):
			from .Bwp_.Csirs import Csirs
			self._csirs = Csirs(self._core, self._base)
		return self._csirs

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Bwp_.Dfreq import Dfreq
			self._dfreq = Dfreq(self._core, self._base)
		return self._dfreq

	@property
	def indicator(self):
		"""indicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_indicator'):
			from .Bwp_.Indicator import Indicator
			self._indicator = Indicator(self._core, self._base)
		return self._indicator

	@property
	def naInd(self):
		"""naInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naInd'):
			from .Bwp_.NaInd import NaInd
			self._naInd = NaInd(self._core, self._base)
		return self._naInd

	@property
	def ncind(self):
		"""ncind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncind'):
			from .Bwp_.Ncind import Ncind
			self._ncind = Ncind(self._core, self._base)
		return self._ncind

	@property
	def pdcch(self):
		"""pdcch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdcch'):
			from .Bwp_.Pdcch import Pdcch
			self._pdcch = Pdcch(self._core, self._base)
		return self._pdcch

	@property
	def pdsch(self):
		"""pdsch commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdsch'):
			from .Bwp_.Pdsch import Pdsch
			self._pdsch = Pdsch(self._core, self._base)
		return self._pdsch

	@property
	def prbOffset(self):
		"""prbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbOffset'):
			from .Bwp_.PrbOffset import PrbOffset
			self._prbOffset = PrbOffset(self._core, self._base)
		return self._prbOffset

	@property
	def pucch(self):
		"""pucch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pucch'):
			from .Bwp_.Pucch import Pucch
			self._pucch = Pucch(self._core, self._base)
		return self._pucch

	@property
	def pusch(self):
		"""pusch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Bwp_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

	@property
	def ratm(self):
		"""ratm commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ratm'):
			from .Bwp_.Ratm import Ratm
			self._ratm = Ratm(self._core, self._base)
		return self._ratm

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .Bwp_.RbNumber import RbNumber
			self._rbNumber = RbNumber(self._core, self._base)
		return self._rbNumber

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .Bwp_.RbOffset import RbOffset
			self._rbOffset = RbOffset(self._core, self._base)
		return self._rbOffset

	@property
	def rnti(self):
		"""rnti commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_rnti'):
			from .Bwp_.Rnti import Rnti
			self._rnti = Rnti(self._core, self._base)
		return self._rnti

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .Bwp_.ScSpacing import ScSpacing
			self._scSpacing = ScSpacing(self._core, self._base)
		return self._scSpacing

	@property
	def srs(self):
		"""srs commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_srs'):
			from .Bwp_.Srs import Srs
			self._srs = Srs(self._core, self._base)
		return self._srs
