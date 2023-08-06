from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Galileo:
	"""Galileo commands group definition. 9 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("galileo", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Galileo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Galileo(self._core, self._base.parent)
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
	def aone(self):
		"""aone commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_aone'):
			from .Galileo_.Aone import Aone
			self._aone = Aone(self._core, self._base)
		return self._aone

	@property
	def atwo(self):
		"""atwo commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_atwo'):
			from .Galileo_.Atwo import Atwo
			self._atwo = Atwo(self._core, self._base)
		return self._atwo

	@property
	def azero(self):
		"""azero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_azero'):
			from .Galileo_.Azero import Azero
			self._azero = Azero(self._core, self._base)
		return self._azero

	@property
	def tot(self):
		"""tot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tot'):
			from .Galileo_.Tot import Tot
			self._tot = Tot(self._core, self._base)
		return self._tot

	@property
	def wnot(self):
		"""wnot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wnot'):
			from .Galileo_.Wnot import Wnot
			self._wnot = Wnot(self._core, self._base)
		return self._wnot
