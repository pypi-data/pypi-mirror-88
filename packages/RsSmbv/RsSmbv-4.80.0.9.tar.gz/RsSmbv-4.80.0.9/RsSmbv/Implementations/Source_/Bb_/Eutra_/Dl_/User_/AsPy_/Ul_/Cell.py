from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 15 total commands, 6 Sub-groups, 2 group commands
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
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Cell_.Append import Append
			self._append = Append(self._core, self._base)
		return self._append

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Cell_.Insert import Insert
			self._insert = Insert(self._core, self._base)
		return self._insert

	@property
	def selement(self):
		"""selement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_selement'):
			from .Cell_.Selement import Selement
			self._selement = Selement(self._core, self._base)
		return self._selement

	@property
	def seqElem(self):
		"""seqElem commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_seqElem'):
			from .Cell_.SeqElem import SeqElem
			self._seqElem = SeqElem(self._core, self._base)
		return self._seqElem

	@property
	def slength(self):
		"""slength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slength'):
			from .Cell_.Slength import Slength
			self._slength = Slength(self._core, self._base)
		return self._slength

	@property
	def vulTxPow(self):
		"""vulTxPow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vulTxPow'):
			from .Cell_.VulTxPow import VulTxPow
			self._vulTxPow = VulTxPow(self._core, self._base)
		return self._vulTxPow

	def delete(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:UL:CELL<ST>:DELete \n
		Deletes the selected table element. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:UL:CELL{stream_cmd_val}:DELete')

	def delete_with_opc(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:UL:CELL<ST>:DELete \n
		Deletes the selected table element. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:UL:CELL{stream_cmd_val}:DELete')

	def reset(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:UL:CELL<ST>:RESet \n
		Resets the DCI table, i.e. removes all table elements. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:UL:CELL{stream_cmd_val}:RESet')

	def reset_with_opc(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:UL:CELL<ST>:RESet \n
		Resets the DCI table, i.e. removes all table elements. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:UL:CELL{stream_cmd_val}:RESet')
