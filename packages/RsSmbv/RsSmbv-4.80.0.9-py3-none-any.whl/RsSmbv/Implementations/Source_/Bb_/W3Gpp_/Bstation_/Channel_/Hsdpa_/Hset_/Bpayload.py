from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bpayload:
	"""Bpayload commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: BitPayloadIx, default value after init: BitPayloadIx.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bpayload", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_bitPayloadIx_get', 'repcap_bitPayloadIx_set', repcap.BitPayloadIx.Nr0)

	def clone(self) -> 'Bpayload':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bpayload(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_bitPayloadIx_set(self, enum_value: repcap.BitPayloadIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BitPayloadIx.Default
		Default value after init: BitPayloadIx.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_bitPayloadIx_get(self) -> repcap.BitPayloadIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, bitPayloadIx=repcap.BitPayloadIx.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:BPAYload<DI> \n
		The command queries the payload of the information bit. This value determines the number of transport layer bits sent in
		each subframe. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param bitPayloadIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bpayload')
			:return: bpayload: float Range: 1 to 5000"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		bitPayloadIx_cmd_val = self._base.get_repcap_cmd_value(bitPayloadIx, repcap.BitPayloadIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:BPAYload{bitPayloadIx_cmd_val}?')
		return Conversions.str_to_float(response)
