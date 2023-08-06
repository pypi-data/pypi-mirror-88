from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal.RepeatedCapability import RepeatedCapability
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Set:
	"""Set commands group definition. 10 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: SrsRsrcSet, default value after init: SrsRsrcSet.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("set", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_srsRsrcSet_get', 'repcap_srsRsrcSet_set', repcap.SrsRsrcSet.Nr0)

	def clone(self) -> 'Set':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Set(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_srsRsrcSet_set(self, enum_value: repcap.SrsRsrcSet) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SrsRsrcSet.Default
		Default value after init: SrsRsrcSet.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_srsRsrcSet_get(self) -> repcap.SrsRsrcSet:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def nresources(self):
		"""nresources commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nresources'):
			from .Set_.Nresources import Nresources
			self._nresources = Nresources(self._core, self._base)
		return self._nresources

	@property
	def res(self):
		"""res commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_res'):
			from .Set_.Res import Res
			self._res = Res(self._core, self._base)
		return self._res
