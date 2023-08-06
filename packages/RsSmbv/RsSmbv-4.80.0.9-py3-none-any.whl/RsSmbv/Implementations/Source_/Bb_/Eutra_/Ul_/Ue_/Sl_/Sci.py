from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sci:
	"""Sci commands group definition. 19 total commands, 19 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sci", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Sci':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sci(self._core, self._base.parent)
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
	def bitData(self):
		"""bitData commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitData'):
			from .Sci_.BitData import BitData
			self._bitData = BitData(self._core, self._base)
		return self._bitData

	@property
	def fhFlag(self):
		"""fhFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fhFlag'):
			from .Sci_.FhFlag import FhFlag
			self._fhFlag = FhFlag(self._core, self._base)
		return self._fhFlag

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .Sci_.FormatPy import FormatPy
			self._formatPy = FormatPy(self._core, self._base)
		return self._formatPy

	@property
	def freqResloc(self):
		"""freqResloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_freqResloc'):
			from .Sci_.FreqResloc import FreqResloc
			self._freqResloc = FreqResloc(self._core, self._base)
		return self._freqResloc

	@property
	def grid(self):
		"""grid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_grid'):
			from .Sci_.Grid import Grid
			self._grid = Grid(self._core, self._base)
		return self._grid

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Sci_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def npscch(self):
		"""npscch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npscch'):
			from .Sci_.Npscch import Npscch
			self._npscch = Npscch(self._core, self._base)
		return self._npscch

	@property
	def pririty(self):
		"""pririty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pririty'):
			from .Sci_.Pririty import Pririty
			self._pririty = Pririty(self._core, self._base)
		return self._pririty

	@property
	def pscPeriod(self):
		"""pscPeriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pscPeriod'):
			from .Sci_.PscPeriod import PscPeriod
			self._pscPeriod = PscPeriod(self._core, self._base)
		return self._pscPeriod

	@property
	def rbahoppAlloc(self):
		"""rbahoppAlloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbahoppAlloc'):
			from .Sci_.RbahoppAlloc import RbahoppAlloc
			self._rbahoppAlloc = RbahoppAlloc(self._core, self._base)
		return self._rbahoppAlloc

	@property
	def rreservation(self):
		"""rreservation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rreservation'):
			from .Sci_.Rreservation import Rreservation
			self._rreservation = Rreservation(self._core, self._base)
		return self._rreservation

	@property
	def sf(self):
		"""sf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sf'):
			from .Sci_.Sf import Sf
			self._sf = Sf(self._core, self._base)
		return self._sf

	@property
	def startSf(self):
		"""startSf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_startSf'):
			from .Sci_.StartSf import StartSf
			self._startSf = StartSf(self._core, self._base)
		return self._startSf

	@property
	def subChannel(self):
		"""subChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subChannel'):
			from .Sci_.SubChannel import SubChannel
			self._subChannel = SubChannel(self._core, self._base)
		return self._subChannel

	@property
	def taInd(self):
		"""taInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taInd'):
			from .Sci_.TaInd import TaInd
			self._taInd = TaInd(self._core, self._base)
		return self._taInd

	@property
	def timGap(self):
		"""timGap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_timGap'):
			from .Sci_.TimGap import TimGap
			self._timGap = TimGap(self._core, self._base)
		return self._timGap

	@property
	def trp(self):
		"""trp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trp'):
			from .Sci_.Trp import Trp
			self._trp = Trp(self._core, self._base)
		return self._trp

	@property
	def txIndex(self):
		"""txIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txIndex'):
			from .Sci_.TxIndex import TxIndex
			self._txIndex = TxIndex(self._core, self._base)
		return self._txIndex

	@property
	def txmode(self):
		"""txmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txmode'):
			from .Sci_.Txmode import Txmode
			self._txmode = Txmode(self._core, self._base)
		return self._txmode
