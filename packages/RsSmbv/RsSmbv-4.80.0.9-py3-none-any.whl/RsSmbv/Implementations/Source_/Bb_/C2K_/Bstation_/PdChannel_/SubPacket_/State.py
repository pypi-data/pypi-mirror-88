from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default, subpacket=repcap.Subpacket.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:SUBPacket<DI>:STATe \n
		This command activates/deactivates the selected sub packet for F_PDCH. Sub packet 1 is always active. \n
			:param state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param subpacket: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubPacket')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subpacket_cmd_val = self._base.get_repcap_cmd_value(subpacket, repcap.Subpacket)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:SUBPacket{subpacket_cmd_val}:STATe {param}')

	def get(self, stream=repcap.Stream.Default, subpacket=repcap.Subpacket.Default) -> bool:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:SUBPacket<DI>:STATe \n
		This command activates/deactivates the selected sub packet for F_PDCH. Sub packet 1 is always active. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param subpacket: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubPacket')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subpacket_cmd_val = self._base.get_repcap_cmd_value(subpacket, repcap.Subpacket)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:SUBPacket{subpacket_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
