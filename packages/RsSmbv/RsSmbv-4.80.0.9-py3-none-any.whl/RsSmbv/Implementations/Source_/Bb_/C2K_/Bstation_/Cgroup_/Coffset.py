from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coffset:
	"""Coffset commands group definition. 31 total commands, 13 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coffset", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Coffset':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Coffset(self._core, self._base.parent)
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
	def ccoding(self):
		"""ccoding commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Coffset_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Coffset_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def derror(self):
		"""derror commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_derror'):
			from .Coffset_.Derror import Derror
			self._derror = Derror(self._core, self._base)
		return self._derror

	@property
	def flength(self):
		"""flength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_flength'):
			from .Coffset_.Flength import Flength
			self._flength = Flength(self._core, self._base)
		return self._flength

	@property
	def lcMask(self):
		"""lcMask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lcMask'):
			from .Coffset_.LcMask import LcMask
			self._lcMask = LcMask(self._core, self._base)
		return self._lcMask

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Coffset_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def qwcode(self):
		"""qwcode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_qwcode'):
			from .Coffset_.Qwcode import Qwcode
			self._qwcode = Qwcode(self._core, self._base)
		return self._qwcode

	@property
	def realtime(self):
		"""realtime commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_realtime'):
			from .Coffset_.Realtime import Realtime
			self._realtime = Realtime(self._core, self._base)
		return self._realtime

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Coffset_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tpc(self):
		"""tpc commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpc'):
			from .Coffset_.Tpc import Tpc
			self._tpc = Tpc(self._core, self._base)
		return self._tpc

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Coffset_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def wcode(self):
		"""wcode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wcode'):
			from .Coffset_.Wcode import Wcode
			self._wcode = Wcode(self._core, self._base)
		return self._wcode

	@property
	def wlength(self):
		"""wlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wlength'):
			from .Coffset_.Wlength import Wlength
			self._wlength = Wlength(self._core, self._base)
		return self._wlength
