from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Toffset:
	"""Toffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("toffset", core, parent)

	def set(self, to_ffset: int, stream=repcap.Stream.Default, subpacket=repcap.Subpacket.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:SUBPacket<DI>:TOFFset \n
		Sets start of the sub packet relative to the start of the packet interval. The offset is entered in slots. Sub packet 1
		has offset 0. The value range for the individual subpackets depends on the settings of the other subpackets. The time
		slot offsets of the other sub packet have to be entered in ascending order. Also, two packets cannot be sent at the same
		time. In total the maximum value depends on the selected packet interval and the number of slots per sub packet as
		follows: Packet Interval/1.25 ms - Number of Slots per Subpacket. \n
			:param to_ffset: integer Range: 0 to max
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param subpacket: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubPacket')"""
		param = Conversions.decimal_value_to_str(to_ffset)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subpacket_cmd_val = self._base.get_repcap_cmd_value(subpacket, repcap.Subpacket)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:SUBPacket{subpacket_cmd_val}:TOFFset {param}')

	def get(self, stream=repcap.Stream.Default, subpacket=repcap.Subpacket.Default) -> int:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:SUBPacket<DI>:TOFFset \n
		Sets start of the sub packet relative to the start of the packet interval. The offset is entered in slots. Sub packet 1
		has offset 0. The value range for the individual subpackets depends on the settings of the other subpackets. The time
		slot offsets of the other sub packet have to be entered in ascending order. Also, two packets cannot be sent at the same
		time. In total the maximum value depends on the selected packet interval and the number of slots per sub packet as
		follows: Packet Interval/1.25 ms - Number of Slots per Subpacket. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param subpacket: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubPacket')
			:return: to_ffset: integer Range: 0 to max"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subpacket_cmd_val = self._base.get_repcap_cmd_value(subpacket, repcap.Subpacket)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:SUBPacket{subpacket_cmd_val}:TOFFset?')
		return Conversions.str_to_int(response)
