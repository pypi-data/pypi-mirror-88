from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Profile:
	"""Profile commands group definition. 7 total commands, 6 Sub-groups, 1 group commands
	Repeated Capability: PseudoRange, default value after init: PseudoRange.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("profile", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_pseudoRange_get', 'repcap_pseudoRange_set', repcap.PseudoRange.Nr1)

	def clone(self) -> 'Profile':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Profile(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_pseudoRange_set(self, enum_value: repcap.PseudoRange) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to PseudoRange.Default
		Default value after init: PseudoRange.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_pseudoRange_get(self) -> repcap.PseudoRange:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Profile_.Append import Append
			self._append = Append(self._core, self._base)
		return self._append

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Profile_.Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Profile_.Insert import Insert
			self._insert = Insert(self._core, self._base)
		return self._insert

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Profile_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Profile_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	@property
	def value(self):
		"""value commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_value'):
			from .Profile_.Value import Value
			self._value = Value(self._core, self._base)
		return self._value

	def delete(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, pseudoRange=repcap.PseudoRange.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:PRERrors:PROFile<GR>:DELete \n
		Deletes the selected pseudorange error. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param pseudoRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		pseudoRange_cmd_val = self._base.get_repcap_cmd_value(pseudoRange, repcap.PseudoRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:PRERrors:PROFile{pseudoRange_cmd_val}:DELete')

	def delete_with_opc(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, pseudoRange=repcap.PseudoRange.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		pseudoRange_cmd_val = self._base.get_repcap_cmd_value(pseudoRange, repcap.PseudoRange)
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:PRERrors:PROFile<GR>:DELete \n
		Deletes the selected pseudorange error. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param pseudoRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:PRERrors:PROFile{pseudoRange_cmd_val}:DELete')
