from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 16 total commands, 9 Sub-groups, 0 group commands
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
	def cdState(self):
		"""cdState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdState'):
			from .Cell_.CdState import CdState
			self._cdState = CdState(self._core, self._base)
		return self._cdState

	@property
	def csirs(self):
		"""csirs commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_csirs'):
			from .Cell_.Csirs import Csirs
			self._csirs = Csirs(self._core, self._base)
		return self._csirs

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Cell_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	@property
	def nzpnum(self):
		"""nzpnum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzpnum'):
			from .Cell_.Nzpnum import Nzpnum
			self._nzpnum = Nzpnum(self._core, self._base)
		return self._nzpnum

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Cell_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Cell_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def periodicity(self):
		"""periodicity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_periodicity'):
			from .Cell_.Periodicity import Periodicity
			self._periodicity = Periodicity(self._core, self._base)
		return self._periodicity

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Cell_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def zpNum(self):
		"""zpNum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpNum'):
			from .Cell_.ZpNum import ZpNum
			self._zpNum = ZpNum(self._core, self._base)
		return self._zpNum
