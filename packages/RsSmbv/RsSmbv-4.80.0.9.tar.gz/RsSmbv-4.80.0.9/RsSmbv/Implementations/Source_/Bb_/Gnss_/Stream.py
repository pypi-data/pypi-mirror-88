from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stream:
	"""Stream commands group definition. 15 total commands, 10 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stream", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Stream':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Stream(self._core, self._base.parent)
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
	def antenna(self):
		"""antenna commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_antenna'):
			from .Stream_.Antenna import Antenna
			self._antenna = Antenna(self._core, self._base)
		return self._antenna

	@property
	def bb(self):
		"""bb commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bb'):
			from .Stream_.Bb import Bb
			self._bb = Bb(self._core, self._base)
		return self._bb

	@property
	def channels(self):
		"""channels commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channels'):
			from .Stream_.Channels import Channels
			self._channels = Channels(self._core, self._base)
		return self._channels

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Stream_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def l1Band(self):
		"""l1Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l1Band'):
			from .Stream_.L1Band import L1Band
			self._l1Band = L1Band(self._core, self._base)
		return self._l1Band

	@property
	def l2Band(self):
		"""l2Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l2Band'):
			from .Stream_.L2Band import L2Band
			self._l2Band = L2Band(self._core, self._base)
		return self._l2Band

	@property
	def l5Band(self):
		"""l5Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l5Band'):
			from .Stream_.L5Band import L5Band
			self._l5Band = L5Band(self._core, self._base)
		return self._l5Band

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Stream_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def rfBand(self):
		"""rfBand commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfBand'):
			from .Stream_.RfBand import RfBand
			self._rfBand = RfBand(self._core, self._base)
		return self._rfBand

	@property
	def vehicle(self):
		"""vehicle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vehicle'):
			from .Stream_.Vehicle import Vehicle
			self._vehicle = Vehicle(self._core, self._base)
		return self._vehicle
