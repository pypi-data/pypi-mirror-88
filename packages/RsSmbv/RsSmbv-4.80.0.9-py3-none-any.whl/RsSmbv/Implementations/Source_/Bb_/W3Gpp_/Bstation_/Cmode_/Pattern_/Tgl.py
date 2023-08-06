from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tgl:
	"""Tgl commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: TransmissionGapLen, default value after init: TransmissionGapLen.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tgl", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_transmissionGapLen_get', 'repcap_transmissionGapLen_set', repcap.TransmissionGapLen.Nr0)

	def clone(self) -> 'Tgl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tgl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_transmissionGapLen_set(self, enum_value: repcap.TransmissionGapLen) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TransmissionGapLen.Default
		Default value after init: TransmissionGapLen.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_transmissionGapLen_get(self) -> repcap.TransmissionGapLen:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, tgl: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, transmissionGapLen=repcap.TransmissionGapLen.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CMODe:PATTern<CH>:TGL<DI> \n
		Sets the transmission gap lengths. \n
			:param tgl: integer Range: 3 to 14
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')
			:param transmissionGapLen: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tgl')"""
		param = Conversions.decimal_value_to_str(tgl)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transmissionGapLen_cmd_val = self._base.get_repcap_cmd_value(transmissionGapLen, repcap.TransmissionGapLen)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CMODe:PATTern{channel_cmd_val}:TGL{transmissionGapLen_cmd_val} {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, transmissionGapLen=repcap.TransmissionGapLen.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CMODe:PATTern<CH>:TGL<DI> \n
		Sets the transmission gap lengths. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')
			:param transmissionGapLen: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tgl')
			:return: tgl: integer Range: 3 to 14"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transmissionGapLen_cmd_val = self._base.get_repcap_cmd_value(transmissionGapLen, repcap.TransmissionGapLen)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CMODe:PATTern{channel_cmd_val}:TGL{transmissionGapLen_cmd_val}?')
		return Conversions.str_to_int(response)
