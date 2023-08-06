from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class V:
	"""V commands group definition. 5 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("v", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'V':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = V(self._core, self._base.parent)
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
	def hilPosition(self):
		"""hilPosition commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hilPosition'):
			from .V_.HilPosition import HilPosition
			self._hilPosition = HilPosition(self._core, self._base)
		return self._hilPosition

	@property
	def rlocation(self):
		"""rlocation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rlocation'):
			from .V_.Rlocation import Rlocation
			self._rlocation = Rlocation(self._core, self._base)
		return self._rlocation

	@property
	def rvelocity(self):
		"""rvelocity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvelocity'):
			from .V_.Rvelocity import Rvelocity
			self._rvelocity = Rvelocity(self._core, self._base)
		return self._rvelocity
