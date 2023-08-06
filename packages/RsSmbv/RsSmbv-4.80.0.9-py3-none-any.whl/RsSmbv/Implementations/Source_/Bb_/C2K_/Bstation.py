from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bstation:
	"""Bstation commands group definition. 55 total commands, 9 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bstation", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Bstation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bstation(self._core, self._base.parent)
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
	def cgroup(self):
		"""cgroup commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cgroup'):
			from .Bstation_.Cgroup import Cgroup
			self._cgroup = Cgroup(self._core, self._base)
		return self._cgroup

	@property
	def dconflict(self):
		"""dconflict commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_dconflict'):
			from .Bstation_.Dconflict import Dconflict
			self._dconflict = Dconflict(self._core, self._base)
		return self._dconflict

	@property
	def pdChannel(self):
		"""pdChannel commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdChannel'):
			from .Bstation_.PdChannel import PdChannel
			self._pdChannel = PdChannel(self._core, self._base)
		return self._pdChannel

	@property
	def pnOffset(self):
		"""pnOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pnOffset'):
			from .Bstation_.PnOffset import PnOffset
			self._pnOffset = PnOffset(self._core, self._base)
		return self._pnOffset

	@property
	def qwset(self):
		"""qwset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qwset'):
			from .Bstation_.Qwset import Qwset
			self._qwset = Qwset(self._core, self._base)
		return self._qwset

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Bstation_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def sync(self):
		"""sync commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_sync'):
			from .Bstation_.Sync import Sync
			self._sync = Sync(self._core, self._base)
		return self._sync

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Bstation_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	@property
	def tdiversity(self):
		"""tdiversity commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdiversity'):
			from .Bstation_.Tdiversity import Tdiversity
			self._tdiversity = Tdiversity(self._core, self._base)
		return self._tdiversity

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation:PRESet \n
		A standardized default for all the base stations (*RST values specified for the commands) . See 'Reset All Base Stations'
		for an overview. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation:PRESet \n
		A standardized default for all the base stations (*RST values specified for the commands) . See 'Reset All Base Stations'
		for an overview. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:C2K:BSTation:PRESet')
