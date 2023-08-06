from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
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
	def dmrs(self):
		"""dmrs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmrs'):
			from .Cell_.Dmrs import Dmrs
			self._dmrs = Dmrs(self._core, self._base)
		return self._dmrs

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Cell_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def seol(self):
		"""seol commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_seol'):
			from .Cell_.Seol import Seol
			self._seol = Seol(self._core, self._base)
		return self._seol

	@property
	def tbal(self):
		"""tbal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbal'):
			from .Cell_.Tbal import Tbal
			self._tbal = Tbal(self._core, self._base)
		return self._tbal

	@property
	def txm(self):
		"""txm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txm'):
			from .Cell_.Txm import Txm
			self._txm = Txm(self._core, self._base)
		return self._txm
