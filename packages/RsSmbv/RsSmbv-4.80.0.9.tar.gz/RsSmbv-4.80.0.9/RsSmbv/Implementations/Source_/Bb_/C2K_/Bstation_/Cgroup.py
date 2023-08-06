from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cgroup:
	"""Cgroup commands group definition. 32 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: ChannelGroup, default value after init: ChannelGroup.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cgroup", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channelGroup_get', 'repcap_channelGroup_set', repcap.ChannelGroup.Nr0)

	def clone(self) -> 'Cgroup':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cgroup(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channelGroup_set(self, enum_value: repcap.ChannelGroup) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ChannelGroup.Default
		Default value after init: ChannelGroup.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channelGroup_get(self) -> repcap.ChannelGroup:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def coffset(self):
		"""coffset commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_coffset'):
			from .Cgroup_.Coffset import Coffset
			self._coffset = Coffset(self._core, self._base)
		return self._coffset

	@property
	def rconfiguration(self):
		"""rconfiguration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rconfiguration'):
			from .Cgroup_.Rconfiguration import Rconfiguration
			self._rconfiguration = Rconfiguration(self._core, self._base)
		return self._rconfiguration
