from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Terminal:
	"""Terminal commands group definition. 52 total commands, 15 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("terminal", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Terminal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Terminal(self._core, self._base.parent)
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
	def ackChannel(self):
		"""ackChannel commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_ackChannel'):
			from .Terminal_.AckChannel import AckChannel
			self._ackChannel = AckChannel(self._core, self._base)
		return self._ackChannel

	@property
	def acycle(self):
		"""acycle commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_acycle'):
			from .Terminal_.Acycle import Acycle
			self._acycle = Acycle(self._core, self._base)
		return self._acycle

	@property
	def apChannel(self):
		"""apChannel commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_apChannel'):
			from .Terminal_.ApChannel import ApChannel
			self._apChannel = ApChannel(self._core, self._base)
		return self._apChannel

	@property
	def dchannel(self):
		"""dchannel commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_dchannel'):
			from .Terminal_.Dchannel import Dchannel
			self._dchannel = Dchannel(self._core, self._base)
		return self._dchannel

	@property
	def dqSpreading(self):
		"""dqSpreading commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dqSpreading'):
			from .Terminal_.DqSpreading import DqSpreading
			self._dqSpreading = DqSpreading(self._core, self._base)
		return self._dqSpreading

	@property
	def drcChannel(self):
		"""drcChannel commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_drcChannel'):
			from .Terminal_.DrcChannel import DrcChannel
			self._drcChannel = DrcChannel(self._core, self._base)
		return self._drcChannel

	@property
	def dscChannel(self):
		"""dscChannel commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dscChannel'):
			from .Terminal_.DscChannel import DscChannel
			self._dscChannel = DscChannel(self._core, self._base)
		return self._dscChannel

	@property
	def imask(self):
		"""imask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imask'):
			from .Terminal_.Imask import Imask
			self._imask = Imask(self._core, self._base)
		return self._imask

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Terminal_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def pchannel(self):
		"""pchannel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pchannel'):
			from .Terminal_.Pchannel import Pchannel
			self._pchannel = Pchannel(self._core, self._base)
		return self._pchannel

	@property
	def plength(self):
		"""plength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plength'):
			from .Terminal_.Plength import Plength
			self._plength = Plength(self._core, self._base)
		return self._plength

	@property
	def qmask(self):
		"""qmask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qmask'):
			from .Terminal_.Qmask import Qmask
			self._qmask = Qmask(self._core, self._base)
		return self._qmask

	@property
	def rriChannel(self):
		"""rriChannel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rriChannel'):
			from .Terminal_.RriChannel import RriChannel
			self._rriChannel = RriChannel(self._core, self._base)
		return self._rriChannel

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Terminal_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def subType(self):
		"""subType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subType'):
			from .Terminal_.SubType import SubType
			self._subType = SubType(self._core, self._base)
		return self._subType
