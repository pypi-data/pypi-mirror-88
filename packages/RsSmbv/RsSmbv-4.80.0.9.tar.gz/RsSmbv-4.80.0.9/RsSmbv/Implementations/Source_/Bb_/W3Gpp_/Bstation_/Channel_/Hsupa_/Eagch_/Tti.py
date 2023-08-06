from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tti:
	"""Tti commands group definition. 3 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: TwoStreams, default value after init: TwoStreams.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tti", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_twoStreams_get', 'repcap_twoStreams_set', repcap.TwoStreams.Nr0)

	def clone(self) -> 'Tti':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tti(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_twoStreams_set(self, enum_value: repcap.TwoStreams) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TwoStreams.Default
		Default value after init: TwoStreams.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_twoStreams_get(self) -> repcap.TwoStreams:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def agScope(self):
		"""agScope commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_agScope'):
			from .Tti_.AgScope import AgScope
			self._agScope = AgScope(self._core, self._base)
		return self._agScope

	@property
	def agvIndex(self):
		"""agvIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_agvIndex'):
			from .Tti_.AgvIndex import AgvIndex
			self._agvIndex = AgvIndex(self._core, self._base)
		return self._agvIndex

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .Tti_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid
