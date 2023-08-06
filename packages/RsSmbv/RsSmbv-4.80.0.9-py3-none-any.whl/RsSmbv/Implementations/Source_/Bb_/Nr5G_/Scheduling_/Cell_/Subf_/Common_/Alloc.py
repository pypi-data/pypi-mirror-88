from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alloc:
	"""Alloc commands group definition. 11 total commands, 11 Sub-groups, 0 group commands
	Repeated Capability: AllocationPerUser, default value after init: AllocationPerUser.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alloc", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_allocationPerUser_get', 'repcap_allocationPerUser_set', repcap.AllocationPerUser.Nr0)

	def clone(self) -> 'Alloc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Alloc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_allocationPerUser_set(self, enum_value: repcap.AllocationPerUser) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AllocationPerUser.Default
		Default value after init: AllocationPerUser.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_allocationPerUser_get(self) -> repcap.AllocationPerUser:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def content(self):
		"""content commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_content'):
			from .Alloc_.Content import Content
			self._content = Content(self._core, self._base)
		return self._content

	@property
	def mod(self):
		"""mod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mod'):
			from .Alloc_.Mod import Mod
			self._mod = Mod(self._core, self._base)
		return self._mod

	@property
	def numerology(self):
		"""numerology commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_numerology'):
			from .Alloc_.Numerology import Numerology
			self._numerology = Numerology(self._core, self._base)
		return self._numerology

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Alloc_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

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
