from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.RepeatedCapability import RepeatedCapability
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Res:
	"""Res commands group definition. 22 total commands, 17 Sub-groups, 0 group commands
	Repeated Capability: SrsRsrcSetRsrc, default value after init: SrsRsrcSetRsrc.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("res", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_srsRsrcSetRsrc_get', 'repcap_srsRsrcSetRsrc_set', repcap.SrsRsrcSetRsrc.Nr0)

	def clone(self) -> 'Res':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Res(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_srsRsrcSetRsrc_set(self, enum_value: repcap.SrsRsrcSetRsrc) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SrsRsrcSetRsrc.Default
		Default value after init: SrsRsrcSetRsrc.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_srsRsrcSetRsrc_get(self) -> repcap.SrsRsrcSetRsrc:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def apMap(self):
		"""apMap commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_apMap'):
			from .Res_.ApMap import ApMap
			self._apMap = ApMap(self._core, self._base)
		return self._apMap

	@property
	def bhop(self):
		"""bhop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bhop'):
			from .Res_.Bhop import Bhop
			self._bhop = Bhop(self._core, self._base)
		return self._bhop

	@property
	def bsrs(self):
		"""bsrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsrs'):
			from .Res_.Bsrs import Bsrs
			self._bsrs = Bsrs(self._core, self._base)
		return self._bsrs

	@property
	def coffset(self):
		"""coffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coffset'):
			from .Res_.Coffset import Coffset
			self._coffset = Coffset(self._core, self._base)
		return self._coffset

	@property
	def csrs(self):
		"""csrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csrs'):
			from .Res_.Csrs import Csrs
			self._csrs = Csrs(self._core, self._base)
		return self._csrs

	@property
	def fpos(self):
		"""fpos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fpos'):
			from .Res_.Fpos import Fpos
			self._fpos = Fpos(self._core, self._base)
		return self._fpos

	@property
	def fqShift(self):
		"""fqShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fqShift'):
			from .Res_.FqShift import FqShift
			self._fqShift = FqShift(self._core, self._base)
		return self._fqShift

	@property
	def naPort(self):
		"""naPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naPort'):
			from .Res_.NaPort import NaPort
			self._naPort = NaPort(self._core, self._base)
		return self._naPort

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Res_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def per(self):
		"""per commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_per'):
			from .Res_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Res_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def ptrs(self):
		"""ptrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptrs'):
			from .Res_.Ptrs import Ptrs
			self._ptrs = Ptrs(self._core, self._base)
		return self._ptrs

	@property
	def refactor(self):
		"""refactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_refactor'):
			from .Res_.Refactor import Refactor
			self._refactor = Refactor(self._core, self._base)
		return self._refactor

	@property
	def seq(self):
		"""seq commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_seq'):
			from .Res_.Seq import Seq
			self._seq = Seq(self._core, self._base)
		return self._seq

	@property
	def spos(self):
		"""spos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spos'):
			from .Res_.Spos import Spos
			self._spos = Spos(self._core, self._base)
		return self._spos

	@property
	def symNumber(self):
		"""symNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symNumber'):
			from .Res_.SymNumber import SymNumber
			self._symNumber = SymNumber(self._core, self._base)
		return self._symNumber

	@property
	def trtComb(self):
		"""trtComb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trtComb'):
			from .Res_.TrtComb import TrtComb
			self._trtComb = TrtComb(self._core, self._base)
		return self._trtComb
