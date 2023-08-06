from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 25 total commands, 12 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		
		self._base.multi_repcap_types = "Stream,CarrierComponent"

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Cell_.Append import Append
			self._append = Append(self._core, self._base)
		return self._append

	@property
	def fmcs(self):
		"""fmcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmcs'):
			from .Cell_.Fmcs import Fmcs
			self._fmcs = Fmcs(self._core, self._base)
		return self._fmcs

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Cell_.Insert import Insert
			self._insert = Insert(self._core, self._base)
		return self._insert

	@property
	def mcsMode(self):
		"""mcsMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsMode'):
			from .Cell_.McsMode import McsMode
			self._mcsMode = McsMode(self._core, self._base)
		return self._mcsMode

	@property
	def rvcSequence(self):
		"""rvcSequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvcSequence'):
			from .Cell_.RvcSequence import RvcSequence
			self._rvcSequence = RvcSequence(self._core, self._base)
		return self._rvcSequence

	@property
	def selement(self):
		"""selement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_selement'):
			from .Cell_.Selement import Selement
			self._selement = Selement(self._core, self._base)
		return self._selement

	@property
	def seqElem(self):
		"""seqElem commands group. 6 Sub-classes, 0 commands."""
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
	def tcr(self):
		"""tcr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcr'):
			from .Cell_.Tcr import Tcr
			self._tcr = Tcr(self._core, self._base)
		return self._tcr

	@property
	def tmod(self):
		"""tmod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmod'):
			from .Cell_.Tmod import Tmod
			self._tmod = Tmod(self._core, self._base)
		return self._tmod

	@property
	def urlCounter(self):
		"""urlCounter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_urlCounter'):
			from .Cell_.UrlCounter import UrlCounter
			self._urlCounter = UrlCounter(self._core, self._base)
		return self._urlCounter

	@property
	def usubframe(self):
		"""usubframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usubframe'):
			from .Cell_.Usubframe import Usubframe
			self._usubframe = Usubframe(self._core, self._base)
		return self._usubframe

	def delete(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:DELete \n
		Deletes the selected table element. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:DELete')

	def delete_with_opc(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:DELete \n
		Deletes the selected table element. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:DELete')

	def reset(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:RESet \n
		Resets the DCI table, i.e. removes all table elements. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:RESet')

	def reset_with_opc(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:RESet \n
		Resets the DCI table, i.e. removes all table elements. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:RESet')
