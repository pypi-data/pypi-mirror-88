from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bwp:
	"""Bwp commands group definition. 120 total commands, 12 Sub-groups, 0 group commands
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
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Bwp_.Dfreq import Dfreq
			self._dfreq = Dfreq(self._core, self._base)
		return self._dfreq

	@property
	def frc(self):
		"""frc commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_frc'):
			from .Bwp_.Frc import Frc
			self._frc = Frc(self._core, self._base)
		return self._frc

	@property
	def indicator(self):
		"""indicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_indicator'):
			from .Bwp_.Indicator import Indicator
			self._indicator = Indicator(self._core, self._base)
		return self._indicator

	@property
	def pdsch(self):
		"""pdsch commands group. 1 Sub-classes, 0 commands."""
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
		"""pucch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pucch'):
			from .Bwp_.Pucch import Pucch
			self._pucch = Pucch(self._core, self._base)
		return self._pucch

	@property
	def pusch(self):
		"""pusch commands group. 15 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Bwp_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

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
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .Bwp_.ScSpacing import ScSpacing
			self._scSpacing = ScSpacing(self._core, self._base)
		return self._scSpacing

	@property
	def srs(self):
		"""srs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_srs'):
			from .Bwp_.Srs import Srs
			self._srs = Srs(self._core, self._base)
		return self._srs

	@property
	def uci(self):
		"""uci commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_uci'):
			from .Bwp_.Uci import Uci
			self._uci = Uci(self._core, self._base)
		return self._uci
