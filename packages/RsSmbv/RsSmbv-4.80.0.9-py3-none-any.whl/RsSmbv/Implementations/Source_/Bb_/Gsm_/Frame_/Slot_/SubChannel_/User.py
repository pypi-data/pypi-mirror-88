from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 27 total commands, 13 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
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
	def attenuation(self):
		"""attenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_attenuation'):
			from .User_.Attenuation import Attenuation
			self._attenuation = Attenuation(self._core, self._base)
		return self._attenuation

	@property
	def dummy(self):
		"""dummy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dummy'):
			from .User_.Dummy import Dummy
			self._dummy = Dummy(self._core, self._base)
		return self._dummy

	@property
	def etsc(self):
		"""etsc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_etsc'):
			from .User_.Etsc import Etsc
			self._etsc = Etsc(self._core, self._base)
		return self._etsc

	@property
	def fcorrection(self):
		"""fcorrection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fcorrection'):
			from .User_.Fcorrection import Fcorrection
			self._fcorrection = Fcorrection(self._core, self._base)
		return self._fcorrection

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .User_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .User_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def predefined(self):
		"""predefined commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .User_.Predefined import Predefined
			self._predefined = Predefined(self._core, self._base)
		return self._predefined

	@property
	def scpiRatio(self):
		"""scpiRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scpiRatio'):
			from .User_.ScpiRatio import ScpiRatio
			self._scpiRatio = ScpiRatio(self._core, self._base)
		return self._scpiRatio

	@property
	def sflag(self):
		"""sflag commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sflag'):
			from .User_.Sflag import Sflag
			self._sflag = Sflag(self._core, self._base)
		return self._sflag

	@property
	def sync(self):
		"""sync commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .User_.Sync import Sync
			self._sync = Sync(self._core, self._base)
		return self._sync

	@property
	def trigger(self):
		"""trigger commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .User_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def ulist(self):
		"""ulist commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_ulist'):
			from .User_.Ulist import Ulist
			self._ulist = Ulist(self._core, self._base)
		return self._ulist

	@property
	def source(self):
		"""source commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_source'):
			from .User_.Source import Source
			self._source = Source(self._core, self._base)
		return self._source
