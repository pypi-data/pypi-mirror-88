from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sspbch:
	"""Sspbch commands group definition. 32 total commands, 15 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sspbch", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Sspbch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sspbch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def bsPeriodicty(self):
		"""bsPeriodicty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsPeriodicty'):
			from .Sspbch_.BsPeriodicty import BsPeriodicty
			self._bsPeriodicty = BsPeriodicty(self._core, self._base)
		return self._bsPeriodicty

	@property
	def case(self):
		"""case commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_case'):
			from .Sspbch_.Case import Case
			self._case = Case(self._core, self._base)
		return self._case

	@property
	def ccoding(self):
		"""ccoding commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Sspbch_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Sspbch_.Dfreq import Dfreq
			self._dfreq = Dfreq(self._core, self._base)
		return self._dfreq

	@property
	def hfrmIdx(self):
		"""hfrmIdx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hfrmIdx'):
			from .Sspbch_.HfrmIdx import HfrmIdx
			self._hfrmIdx = HfrmIdx(self._core, self._base)
		return self._hfrmIdx

	@property
	def lpy(self):
		"""lpy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lpy'):
			from .Sspbch_.Lpy import Lpy
			self._lpy = Lpy(self._core, self._base)
		return self._lpy

	@property
	def mib(self):
		"""mib commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_mib'):
			from .Sspbch_.Mib import Mib
			self._mib = Mib(self._core, self._base)
		return self._mib

	@property
	def position(self):
		"""position commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_position'):
			from .Sspbch_.Position import Position
			self._position = Position(self._core, self._base)
		return self._position

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Sspbch_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def pssPow(self):
		"""pssPow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pssPow'):
			from .Sspbch_.PssPow import PssPow
			self._pssPow = PssPow(self._core, self._base)
		return self._pssPow

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .Sspbch_.RbOffset import RbOffset
			self._rbOffset = RbOffset(self._core, self._base)
		return self._rbOffset

	@property
	def scOffset(self):
		"""scOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scOffset'):
			from .Sspbch_.ScOffset import ScOffset
			self._scOffset = ScOffset(self._core, self._base)
		return self._scOffset

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .Sspbch_.ScSpacing import ScSpacing
			self._scSpacing = ScSpacing(self._core, self._base)
		return self._scSpacing

	@property
	def ssspow(self):
		"""ssspow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssspow'):
			from .Sspbch_.Ssspow import Ssspow
			self._ssspow = Ssspow(self._core, self._base)
		return self._ssspow

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Sspbch_.State import State
			self._state = State(self._core, self._base)
		return self._state
