from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 12 total commands, 12 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
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
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Cell_.Bw import Bw
			self._bw = Bw(self._core, self._base)
		return self._bw

	@property
	def csrs(self):
		"""csrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csrs'):
			from .Cell_.Csrs import Csrs
			self._csrs = Csrs(self._core, self._base)
		return self._csrs

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Cell_.Dfreq import Dfreq
			self._dfreq = Dfreq(self._core, self._base)
		return self._dfreq

	@property
	def dmrs(self):
		"""dmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmrs'):
			from .Cell_.Dmrs import Dmrs
			self._dmrs = Dmrs(self._core, self._base)
		return self._dmrs

	@property
	def duplexing(self):
		"""duplexing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duplexing'):
			from .Cell_.Duplexing import Duplexing
			self._duplexing = Duplexing(self._core, self._base)
		return self._duplexing

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Cell_.Id import Id
			self._id = Id(self._core, self._base)
		return self._id

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Cell_.Index import Index
			self._index = Index(self._core, self._base)
		return self._index

	@property
	def spsConf(self):
		"""spsConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spsConf'):
			from .Cell_.SpsConf import SpsConf
			self._spsConf = SpsConf(self._core, self._base)
		return self._spsConf

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Cell_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def suConfiguration(self):
		"""suConfiguration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_suConfiguration'):
			from .Cell_.SuConfiguration import SuConfiguration
			self._suConfiguration = SuConfiguration(self._core, self._base)
		return self._suConfiguration

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Cell_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	@property
	def udConf(self):
		"""udConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_udConf'):
			from .Cell_.UdConf import UdConf
			self._udConf = UdConf(self._core, self._base)
		return self._udConf
