from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class M11T:
	"""M11T commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("m11T", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'M11T':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = M11T(self._core, self._base.parent)
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
	def foffset(self):
		"""foffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_foffset'):
			from .M11T_.Foffset import Foffset
			self._foffset = Foffset(self._core, self._base)
		return self._foffset

	@property
	def lpair(self):
		"""lpair commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lpair'):
			from .M11T_.Lpair import Lpair
			self._lpair = Lpair(self._core, self._base)
		return self._lpair

	@property
	def mbytes(self):
		"""mbytes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mbytes'):
			from .M11T_.Mbytes import Mbytes
			self._mbytes = Mbytes(self._core, self._base)
		return self._mbytes

	@property
	def rframe(self):
		"""rframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rframe'):
			from .M11T_.Rframe import Rframe
			self._rframe = Rframe(self._core, self._base)
		return self._rframe

	@property
	def slot(self):
		"""slot commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .M11T_.Slot import Slot
			self._slot = Slot(self._core, self._base)
		return self._slot
