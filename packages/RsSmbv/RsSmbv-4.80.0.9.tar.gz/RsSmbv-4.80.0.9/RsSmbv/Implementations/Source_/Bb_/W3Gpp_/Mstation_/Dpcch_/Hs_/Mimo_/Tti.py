from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tti:
	"""Tti commands group definition. 4 total commands, 4 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tti", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Tti':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tti(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def cqi(self):
		"""cqi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cqi'):
			from .Tti_.Cqi import Cqi
			self._cqi = Cqi(self._core, self._base)
		return self._cqi

	@property
	def cqiType(self):
		"""cqiType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cqiType'):
			from .Tti_.CqiType import CqiType
			self._cqiType = CqiType(self._core, self._base)
		return self._cqiType

	@property
	def hack(self):
		"""hack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hack'):
			from .Tti_.Hack import Hack
			self._hack = Hack(self._core, self._base)
		return self._hack

	@property
	def pci(self):
		"""pci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pci'):
			from .Tti_.Pci import Pci
			self._pci = Pci(self._core, self._base)
		return self._pci
