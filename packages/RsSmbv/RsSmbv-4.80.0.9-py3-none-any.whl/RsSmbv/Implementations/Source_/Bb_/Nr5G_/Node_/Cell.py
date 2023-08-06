from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 106 total commands, 23 Sub-groups, 0 group commands
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
	def afState(self):
		"""afState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_afState'):
			from .Cell_.AfState import AfState
			self._afState = AfState(self._core, self._base)
		return self._afState

	@property
	def cardeply(self):
		"""cardeply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cardeply'):
			from .Cell_.Cardeply import Cardeply
			self._cardeply = Cardeply(self._core, self._base)
		return self._cardeply

	@property
	def cbw(self):
		"""cbw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbw'):
			from .Cell_.Cbw import Cbw
			self._cbw = Cbw(self._core, self._base)
		return self._cbw

	@property
	def cellid(self):
		"""cellid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cellid'):
			from .Cell_.Cellid import Cellid
			self._cellid = Cellid(self._core, self._base)
		return self._cellid

	@property
	def cif(self):
		"""cif commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cif'):
			from .Cell_.Cif import Cif
			self._cif = Cif(self._core, self._base)
		return self._cif

	@property
	def cifPresent(self):
		"""cifPresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cifPresent'):
			from .Cell_.CifPresent import CifPresent
			self._cifPresent = CifPresent(self._core, self._base)
		return self._cifPresent

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Cell_.Dfreq import Dfreq
			self._dfreq = Dfreq(self._core, self._base)
		return self._dfreq

	@property
	def dumRes(self):
		"""dumRes commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_dumRes'):
			from .Cell_.DumRes import DumRes
			self._dumRes = DumRes(self._core, self._base)
		return self._dumRes

	@property
	def lte(self):
		"""lte commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_lte'):
			from .Cell_.Lte import Lte
			self._lte = Lte(self._core, self._base)
		return self._lte

	@property
	def mapped(self):
		"""mapped commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mapped'):
			from .Cell_.Mapped import Mapped
			self._mapped = Mapped(self._core, self._base)
		return self._mapped

	@property
	def n1Id(self):
		"""n1Id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n1Id'):
			from .Cell_.N1Id import N1Id
			self._n1Id = N1Id(self._core, self._base)
		return self._n1Id

	@property
	def n2Id(self):
		"""n2Id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Id'):
			from .Cell_.N2Id import N2Id
			self._n2Id = N2Id(self._core, self._base)
		return self._n2Id

	@property
	def nsspbch(self):
		"""nsspbch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsspbch'):
			from .Cell_.Nsspbch import Nsspbch
			self._nsspbch = Nsspbch(self._core, self._base)
		return self._nsspbch

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Cell_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def pcFreq(self):
		"""pcFreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcFreq'):
			from .Cell_.PcFreq import PcFreq
			self._pcFreq = PcFreq(self._core, self._base)
		return self._pcFreq

	@property
	def prs(self):
		"""prs commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_prs'):
			from .Cell_.Prs import Prs
			self._prs = Prs(self._core, self._base)
		return self._prs

	@property
	def rpow(self):
		"""rpow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpow'):
			from .Cell_.Rpow import Rpow
			self._rpow = Rpow(self._core, self._base)
		return self._rpow

	@property
	def schby(self):
		"""schby commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_schby'):
			from .Cell_.Schby import Schby
			self._schby = Schby(self._core, self._base)
		return self._schby

	@property
	def sspbch(self):
		"""sspbch commands group. 15 Sub-classes, 0 commands."""
		if not hasattr(self, '_sspbch'):
			from .Cell_.Sspbch import Sspbch
			self._sspbch = Sspbch(self._core, self._base)
		return self._sspbch

	@property
	def syInfo(self):
		"""syInfo commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_syInfo'):
			from .Cell_.SyInfo import SyInfo
			self._syInfo = SyInfo(self._core, self._base)
		return self._syInfo

	@property
	def taoffset(self):
		"""taoffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taoffset'):
			from .Cell_.Taoffset import Taoffset
			self._taoffset = Taoffset(self._core, self._base)
		return self._taoffset

	@property
	def tapos(self):
		"""tapos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tapos'):
			from .Cell_.Tapos import Tapos
			self._tapos = Tapos(self._core, self._base)
		return self._tapos

	@property
	def txbw(self):
		"""txbw commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_txbw'):
			from .Cell_.Txbw import Txbw
			self._txbw = Txbw(self._core, self._base)
		return self._txbw
