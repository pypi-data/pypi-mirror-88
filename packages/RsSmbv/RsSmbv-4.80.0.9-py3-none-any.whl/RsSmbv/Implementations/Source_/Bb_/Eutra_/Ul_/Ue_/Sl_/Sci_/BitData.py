from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BitData:
	"""BitData commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bitData", core, parent)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SCI<CH>:BITData \n
		Queries the resulting bit data as configured with the [:SOURce<hw>]:BB:EUTRa:UL:UE<st>:SL:SCI<ch0> commands. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sci')
			:return: bit_data: bit pattern"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SCI{channel_cmd_val}:BITData?')
		return Conversions.str_to_str_list(response)
