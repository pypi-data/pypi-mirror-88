from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Burst:
	"""Burst commands group definition. 7 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("burst", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Burst':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Burst(self._core, self._base.parent)
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
	def c1Mode(self):
		"""c1Mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_c1Mode'):
			from .Burst_.C1Mode import C1Mode
			self._c1Mode = C1Mode(self._core, self._base)
		return self._c1Mode

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Burst_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	@property
	def ensFrame(self):
		"""ensFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ensFrame'):
			from .Burst_.EnsFrame import EnsFrame
			self._ensFrame = EnsFrame(self._core, self._base)
		return self._ensFrame

	@property
	def epdcch(self):
		"""epdcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_epdcch'):
			from .Burst_.Epdcch import Epdcch
			self._epdcch = Epdcch(self._core, self._base)
		return self._epdcch

	@property
	def lsfSymbols(self):
		"""lsfSymbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lsfSymbols'):
			from .Burst_.LsfSymbols import LsfSymbols
			self._lsfSymbols = LsfSymbols(self._core, self._base)
		return self._lsfSymbols

	@property
	def stsFrame(self):
		"""stsFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsFrame'):
			from .Burst_.StsFrame import StsFrame
			self._stsFrame = StsFrame(self._core, self._base)
		return self._stsFrame

	@property
	def stslot(self):
		"""stslot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stslot'):
			from .Burst_.Stslot import Stslot
			self._stslot = Stslot(self._core, self._base)
		return self._stslot
