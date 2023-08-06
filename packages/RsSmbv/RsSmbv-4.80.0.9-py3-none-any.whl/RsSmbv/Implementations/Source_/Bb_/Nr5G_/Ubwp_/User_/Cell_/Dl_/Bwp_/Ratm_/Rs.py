from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rs:
	"""Rs commands group definition. 7 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: RateSetting, default value after init: RateSetting.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rs", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_rateSetting_get', 'repcap_rateSetting_set', repcap.RateSetting.Nr0)

	def clone(self) -> 'Rs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_rateSetting_set(self, enum_value: repcap.RateSetting) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to RateSetting.Default
		Default value after init: RateSetting.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_rateSetting_get(self) -> repcap.RateSetting:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def grid(self):
		"""grid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_grid'):
			from .Rs_.Grid import Grid
			self._grid = Grid(self._core, self._base)
		return self._grid

	@property
	def per(self):
		"""per commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_per'):
			from .Rs_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def perPatt(self):
		"""perPatt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_perPatt'):
			from .Rs_.PerPatt import PerPatt
			self._perPatt = PerPatt(self._core, self._base)
		return self._perPatt

	@property
	def rbdlist(self):
		"""rbdlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbdlist'):
			from .Rs_.Rbdlist import Rbdlist
			self._rbdlist = Rbdlist(self._core, self._base)
		return self._rbdlist

	@property
	def rbpAtt(self):
		"""rbpAtt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbpAtt'):
			from .Rs_.RbpAtt import RbpAtt
			self._rbpAtt = RbpAtt(self._core, self._base)
		return self._rbpAtt

	@property
	def slot(self):
		"""slot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slot'):
			from .Rs_.Slot import Slot
			self._slot = Slot(self._core, self._base)
		return self._slot

	@property
	def sltPatt(self):
		"""sltPatt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sltPatt'):
			from .Rs_.SltPatt import SltPatt
			self._sltPatt = SltPatt(self._core, self._base)
		return self._sltPatt
