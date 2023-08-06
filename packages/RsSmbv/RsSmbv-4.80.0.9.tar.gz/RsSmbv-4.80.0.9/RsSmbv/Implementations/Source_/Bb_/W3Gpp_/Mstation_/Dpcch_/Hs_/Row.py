from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Row:
	"""Row commands group definition. 11 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("row", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Row':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Row(self._core, self._base.parent)
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
			from .Row_.Cqi import Cqi
			self._cqi = Cqi(self._core, self._base)
		return self._cqi

	@property
	def hack(self):
		"""hack commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_hack'):
			from .Row_.Hack import Hack
			self._hack = Hack(self._core, self._base)
		return self._hack

	@property
	def pcqi(self):
		"""pcqi commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcqi'):
			from .Row_.Pcqi import Pcqi
			self._pcqi = Pcqi(self._core, self._base)
		return self._pcqi

	@property
	def poHack(self):
		"""poHack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poHack'):
			from .Row_.PoHack import PoHack
			self._poHack = PoHack(self._core, self._base)
		return self._poHack

	@property
	def popCqi(self):
		"""popCqi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_popCqi'):
			from .Row_.PopCqi import PopCqi
			self._popCqi = PopCqi(self._core, self._base)
		return self._popCqi
