from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sbas:
	"""Sbas commands group definition. 99 total commands, 6 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sbas", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Sbas':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sbas(self._core, self._base.parent)
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
	def egnos(self):
		"""egnos commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_egnos'):
			from .Sbas_.Egnos import Egnos
			self._egnos = Egnos(self._core, self._base)
		return self._egnos

	@property
	def gagan(self):
		"""gagan commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gagan'):
			from .Sbas_.Gagan import Gagan
			self._gagan = Gagan(self._core, self._base)
		return self._gagan

	@property
	def msas(self):
		"""msas commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_msas'):
			from .Sbas_.Msas import Msas
			self._msas = Msas(self._core, self._base)
		return self._msas

	@property
	def signal(self):
		"""signal commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_signal'):
			from .Sbas_.Signal import Signal
			self._signal = Signal(self._core, self._base)
		return self._signal

	@property
	def waas(self):
		"""waas commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_waas'):
			from .Sbas_.Waas import Waas
			self._waas = Waas(self._core, self._base)
		return self._waas

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Sbas_.State import State
			self._state = State(self._core, self._base)
		return self._state
