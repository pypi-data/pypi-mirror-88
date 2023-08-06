from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 22 total commands, 11 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
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
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .User_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def drclock(self):
		"""drclock commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_drclock'):
			from .User_.Drclock import Drclock
			self._drclock = Drclock(self._core, self._base)
		return self._drclock

	@property
	def harq(self):
		"""harq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .User_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def ifactor(self):
		"""ifactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ifactor'):
			from .User_.Ifactor import Ifactor
			self._ifactor = Ifactor(self._core, self._base)
		return self._ifactor

	@property
	def mac(self):
		"""mac commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mac'):
			from .User_.Mac import Mac
			self._mac = Mac(self._core, self._base)
		return self._mac

	@property
	def packet(self):
		"""packet commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_packet'):
			from .User_.Packet import Packet
			self._packet = Packet(self._core, self._base)
		return self._packet

	@property
	def psize(self):
		"""psize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psize'):
			from .User_.Psize import Psize
			self._psize = Psize(self._core, self._base)
		return self._psize

	@property
	def rate(self):
		"""rate commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .User_.Rate import Rate
			self._rate = Rate(self._core, self._base)
		return self._rate

	@property
	def rpc(self):
		"""rpc commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_rpc'):
			from .User_.Rpc import Rpc
			self._rpc = Rpc(self._core, self._base)
		return self._rpc

	@property
	def scount(self):
		"""scount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scount'):
			from .User_.Scount import Scount
			self._scount = Scount(self._core, self._base)
		return self._scount

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .User_.State import State
			self._state = State(self._core, self._base)
		return self._state
