from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 7 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Output':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Output(self._core, self._base.parent)
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
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Output_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	@property
	def foffset(self):
		"""foffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_foffset'):
			from .Output_.Foffset import Foffset
			self._foffset = Foffset(self._core, self._base)
		return self._foffset

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Output_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def offTime(self):
		"""offTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offTime'):
			from .Output_.OffTime import OffTime
			self._offTime = OffTime(self._core, self._base)
		return self._offTime

	@property
	def ontime(self):
		"""ontime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ontime'):
			from .Output_.Ontime import Ontime
			self._ontime = Ontime(self._core, self._base)
		return self._ontime

	@property
	def period(self):
		"""period commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_period'):
			from .Output_.Period import Period
			self._period = Period(self._core, self._base)
		return self._period

	@property
	def roffset(self):
		"""roffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_roffset'):
			from .Output_.Roffset import Roffset
			self._roffset = Roffset(self._core, self._base)
		return self._roffset
