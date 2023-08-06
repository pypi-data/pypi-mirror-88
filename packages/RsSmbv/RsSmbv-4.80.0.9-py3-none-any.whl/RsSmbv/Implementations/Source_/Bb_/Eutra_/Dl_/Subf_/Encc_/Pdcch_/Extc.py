from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extc:
	"""Extc commands group definition. 67 total commands, 9 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extc", core, parent)

	def clone(self) -> 'Extc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Extc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Extc_.Append import Append
			self._append = Append(self._core, self._base)
		return self._append

	@property
	def conflicts(self):
		"""conflicts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflicts'):
			from .Extc_.Conflicts import Conflicts
			self._conflicts = Conflicts(self._core, self._base)
		return self._conflicts

	@property
	def down(self):
		"""down commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_down'):
			from .Extc_.Down import Down
			self._down = Down(self._core, self._base)
		return self._down

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Extc_.Insert import Insert
			self._insert = Insert(self._core, self._base)
		return self._insert

	@property
	def item(self):
		"""item commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_item'):
			from .Extc_.Item import Item
			self._item = Item(self._core, self._base)
		return self._item

	@property
	def sitem(self):
		"""sitem commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sitem'):
			from .Extc_.Sitem import Sitem
			self._sitem = Sitem(self._core, self._base)
		return self._sitem

	@property
	def solve(self):
		"""solve commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_solve'):
			from .Extc_.Solve import Solve
			self._solve = Solve(self._core, self._base)
		return self._solve

	@property
	def uitems(self):
		"""uitems commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uitems'):
			from .Extc_.Uitems import Uitems
			self._uitems = Uitems(self._core, self._base)
		return self._uitems

	@property
	def up(self):
		"""up commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_up'):
			from .Extc_.Up import Up
			self._up = Up(self._core, self._base)
		return self._up

	def delete(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:DELete \n
		Deletes the selected row. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:DELete')

	def delete_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:DELete \n
		Deletes the selected row. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:DELete')

	def reset(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:RESet \n
		Resets the table. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:RESet')

	def reset_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:RESet \n
		Resets the table. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:RESet')
