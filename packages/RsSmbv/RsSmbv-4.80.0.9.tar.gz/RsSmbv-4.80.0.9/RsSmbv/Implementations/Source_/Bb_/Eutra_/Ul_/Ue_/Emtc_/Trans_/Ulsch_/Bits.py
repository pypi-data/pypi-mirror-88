from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bits:
	"""Bits commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bits", core, parent)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:TRANs<CH>:ULSCh:BITS \n
		Queries the number of physical bits used for UL-SCH transmission. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: phys_bit_ulsch: integer Range: 0 to 1E5"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:EMTC:TRANs{channel_cmd_val}:ULSCh:BITS?')
		return Conversions.str_to_int(response)
