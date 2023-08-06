from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alloc:
	"""Alloc commands group definition. 16 total commands, 15 Sub-groups, 0 group commands"""

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
	def ncw(self):
		"""ncw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncw'):
			from .Alloc_.Ncw import Ncw
			self._ncw = Ncw(self._core, self._base)
		return self._ncw

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Alloc_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

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
	def resAlloc(self):
		"""resAlloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resAlloc'):
			from .Alloc_.ResAlloc import ResAlloc
			self._resAlloc = ResAlloc(self._core, self._base)
		return self._resAlloc

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
	def sosf(self):
		"""sosf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sosf'):
			from .Alloc_.Sosf import Sosf
			self._sosf = Sosf(self._core, self._base)
		return self._sosf

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
		"""cw commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cw'):
			from .Alloc_.Cw import Cw
			self._cw = Cw(self._core, self._base)
		return self._cw
