from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wcodes:
	"""Wcodes commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wcodes", core, parent)

	def get(self, stream=repcap.Stream.Default, subpacket=repcap.Subpacket.Default) -> List[int]:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:SUBPacket<DI>:WCODes \n
		The command queries the resulting Walsh codes for the selected sub packet of F-PDCH. Packet channels may be assigned to
		more than one code channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param subpacket: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubPacket')
			:return: wcodes: string"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subpacket_cmd_val = self._base.get_repcap_cmd_value(subpacket, repcap.Subpacket)
		response = self._core.io.query_bin_or_ascii_int_list(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:SUBPacket{subpacket_cmd_val}:WCODes?')
		return response
