from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vdb:
	"""Vdb commands group definition. 134 total commands, 12 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vdb", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Vdb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Vdb(self._core, self._base.parent)
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
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Vdb_.Append import Append
			self._append = Append(self._core, self._base)
		return self._append

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Vdb_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dlength(self):
		"""dlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlength'):
			from .Vdb_.Dlength import Dlength
			self._dlength = Dlength(self._core, self._base)
		return self._dlength

	@property
	def fnumber(self):
		"""fnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fnumber'):
			from .Vdb_.Fnumber import Fnumber
			self._fnumber = Fnumber(self._core, self._base)
		return self._fnumber

	@property
	def gid(self):
		"""gid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gid'):
			from .Vdb_.Gid import Gid
			self._gid = Gid(self._core, self._base)
		return self._gid

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Vdb_.Insert import Insert
			self._insert = Insert(self._core, self._base)
		return self._insert

	@property
	def mconfig(self):
		"""mconfig commands group. 54 Sub-classes, 0 commands."""
		if not hasattr(self, '_mconfig'):
			from .Vdb_.Mconfig import Mconfig
			self._mconfig = Mconfig(self._core, self._base)
		return self._mconfig

	@property
	def rid(self):
		"""rid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rid'):
			from .Vdb_.Rid import Rid
			self._rid = Rid(self._core, self._base)
		return self._rid

	@property
	def sch(self):
		"""sch commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_sch'):
			from .Vdb_.Sch import Sch
			self._sch = Sch(self._core, self._base)
		return self._sch

	@property
	def sgid(self):
		"""sgid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgid'):
			from .Vdb_.Sgid import Sgid
			self._sgid = Sgid(self._core, self._base)
		return self._sgid

	@property
	def ssid(self):
		"""ssid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssid'):
			from .Vdb_.Ssid import Ssid
			self._ssid = Ssid(self._core, self._base)
		return self._ssid

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Vdb_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def delete(self, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:DELete \n
		Deletes the selected VDB. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:DELete')

	def delete_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:DELete \n
		Deletes the selected VDB. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:DELete')
