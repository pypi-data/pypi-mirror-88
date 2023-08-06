from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alloc:
	"""Alloc commands group definition. 328 total commands, 25 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alloc", core, parent)

	def clone(self) -> 'Alloc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Alloc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def apMap(self):
		"""apMap commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_apMap'):
			from .Alloc_.ApMap import ApMap
			self._apMap = ApMap(self._core, self._base)
		return self._apMap

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Alloc_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def content(self):
		"""content commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_content'):
			from .Alloc_.Content import Content
			self._content = Content(self._core, self._base)
		return self._content

	@property
	def copyTo(self):
		"""copyTo commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_copyTo'):
			from .Alloc_.CopyTo import CopyTo
			self._copyTo = CopyTo(self._core, self._base)
		return self._copyTo

	@property
	def cs(self):
		"""cs commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_cs'):
			from .Alloc_.Cs import Cs
			self._cs = Cs(self._core, self._base)
		return self._cs

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Alloc_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Alloc_.Fmt import Fmt
			self._fmt = Fmt(self._core, self._base)
		return self._fmt

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Alloc_.Info import Info
			self._info = Info(self._core, self._base)
		return self._info

	@property
	def mapType(self):
		"""mapType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mapType'):
			from .Alloc_.MapType import MapType
			self._mapType = MapType(self._core, self._base)
		return self._mapType

	@property
	def nap(self):
		"""nap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nap'):
			from .Alloc_.Nap import Nap
			self._nap = Nap(self._core, self._base)
		return self._nap

	@property
	def pdsch(self):
		"""pdsch commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdsch'):
			from .Alloc_.Pdsch import Pdsch
			self._pdsch = Pdsch(self._core, self._base)
		return self._pdsch

	@property
	def period(self):
		"""period commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_period'):
			from .Alloc_.Period import Period
			self._period = Period(self._core, self._base)
		return self._period

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Alloc_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def prach(self):
		"""prach commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_prach'):
			from .Alloc_.Prach import Prach
			self._prach = Prach(self._core, self._base)
		return self._prach

	@property
	def pucch(self):
		"""pucch commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_pucch'):
			from .Alloc_.Pucch import Pucch
			self._pucch = Pucch(self._core, self._base)
		return self._pucch

	@property
	def pusch(self):
		"""pusch commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Alloc_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .Alloc_.RbNumber import RbNumber
			self._rbNumber = RbNumber(self._core, self._base)
		return self._rbNumber

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .Alloc_.RbOffset import RbOffset
			self._rbOffset = RbOffset(self._core, self._base)
		return self._rbOffset

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetitions'):
			from .Alloc_.Repetitions import Repetitions
			self._repetitions = Repetitions(self._core, self._base)
		return self._repetitions

	@property
	def slot(self):
		"""slot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slot'):
			from .Alloc_.Slot import Slot
			self._slot = Slot(self._core, self._base)
		return self._slot

	@property
	def sltFmt(self):
		"""sltFmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sltFmt'):
			from .Alloc_.SltFmt import SltFmt
			self._sltFmt = SltFmt(self._core, self._base)
		return self._sltFmt

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Alloc_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def symNumber(self):
		"""symNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symNumber'):
			from .Alloc_.SymNumber import SymNumber
			self._symNumber = SymNumber(self._core, self._base)
		return self._symNumber

	@property
	def symOffset(self):
		"""symOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symOffset'):
			from .Alloc_.SymOffset import SymOffset
			self._symOffset = SymOffset(self._core, self._base)
		return self._symOffset

	@property
	def cw(self):
		"""cw commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_cw'):
			from .Alloc_.Cw import Cw
			self._cw = Cw(self._core, self._base)
		return self._cw
