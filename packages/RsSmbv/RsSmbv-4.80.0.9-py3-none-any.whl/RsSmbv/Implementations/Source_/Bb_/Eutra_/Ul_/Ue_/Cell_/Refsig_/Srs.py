from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Srs:
	"""Srs commands group definition. 16 total commands, 16 Sub-groups, 0 group commands
	Repeated Capability: SoundRefSignalIx, default value after init: SoundRefSignalIx.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srs", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_soundRefSignalIx_get', 'repcap_soundRefSignalIx_set', repcap.SoundRefSignalIx.Nr0)

	def clone(self) -> 'Srs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Srs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_soundRefSignalIx_set(self, enum_value: repcap.SoundRefSignalIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SoundRefSignalIx.Default
		Default value after init: SoundRefSignalIx.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_soundRefSignalIx_get(self) -> repcap.SoundRefSignalIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def bhop(self):
		"""bhop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bhop'):
			from .Srs_.Bhop import Bhop
			self._bhop = Bhop(self._core, self._base)
		return self._bhop

	@property
	def bsrs(self):
		"""bsrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsrs'):
			from .Srs_.Bsrs import Bsrs
			self._bsrs = Bsrs(self._core, self._base)
		return self._bsrs

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .Srs_.CycShift import CycShift
			self._cycShift = CycShift(self._core, self._base)
		return self._cycShift

	@property
	def isrs(self):
		"""isrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isrs'):
			from .Srs_.Isrs import Isrs
			self._isrs = Isrs(self._core, self._base)
		return self._isrs

	@property
	def naPort(self):
		"""naPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naPort'):
			from .Srs_.NaPort import NaPort
			self._naPort = NaPort(self._core, self._base)
		return self._naPort

	@property
	def nktc(self):
		"""nktc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nktc'):
			from .Srs_.Nktc import Nktc
			self._nktc = Nktc(self._core, self._base)
		return self._nktc

	@property
	def nrrc(self):
		"""nrrc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrrc'):
			from .Srs_.Nrrc import Nrrc
			self._nrrc = Nrrc(self._core, self._base)
		return self._nrrc

	@property
	def ntrans(self):
		"""ntrans commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntrans'):
			from .Srs_.Ntrans import Ntrans
			self._ntrans = Ntrans(self._core, self._base)
		return self._ntrans

	@property
	def powOffset(self):
		"""powOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_powOffset'):
			from .Srs_.PowOffset import PowOffset
			self._powOffset = PowOffset(self._core, self._base)
		return self._powOffset

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Srs_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def subf(self):
		"""subf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subf'):
			from .Srs_.Subf import Subf
			self._subf = Subf(self._core, self._base)
		return self._subf

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Srs_.Toffset import Toffset
			self._toffset = Toffset(self._core, self._base)
		return self._toffset

	@property
	def trComb(self):
		"""trComb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trComb'):
			from .Srs_.TrComb import TrComb
			self._trComb = TrComb(self._core, self._base)
		return self._trComb

	@property
	def tsrs(self):
		"""tsrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsrs'):
			from .Srs_.Tsrs import Tsrs
			self._tsrs = Tsrs(self._core, self._base)
		return self._tsrs

	@property
	def tt0(self):
		"""tt0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tt0'):
			from .Srs_.Tt0 import Tt0
			self._tt0 = Tt0(self._core, self._base)
		return self._tt0

	@property
	def upptsadd(self):
		"""upptsadd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_upptsadd'):
			from .Srs_.Upptsadd import Upptsadd
			self._upptsadd = Upptsadd(self._core, self._base)
		return self._upptsadd
