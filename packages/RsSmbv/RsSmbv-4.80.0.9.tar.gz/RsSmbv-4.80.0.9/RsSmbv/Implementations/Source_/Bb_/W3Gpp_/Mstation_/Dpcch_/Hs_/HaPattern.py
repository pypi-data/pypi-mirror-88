from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HaPattern:
	"""HaPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("haPattern", core, parent)

	def set(self, ha_pattern: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:HAPattern \n
		(Up to Release 7) The command enters the pattern for the HARQ-ACK field (Hybrid-ARQ Acknowledgement) . One bit is used
		per HS-DPCCH packet. \n
			:param ha_pattern: string The pattern is entered as string, the maximum number of entries is 32. Three different characters are permitted. 1 The HARQ ACK is sent (ACK) . Transmission was successful and correct. 0 The NACK is sent (NACK) . Transmission was not correct. With an NACK, the UE requests retransmission of the incorrect data. - Nothing is sent. Transmission is interrupted (Discontinuous Transmission, DTX) .
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.value_to_quoted_str(ha_pattern)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:HAPattern {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:HAPattern \n
		(Up to Release 7) The command enters the pattern for the HARQ-ACK field (Hybrid-ARQ Acknowledgement) . One bit is used
		per HS-DPCCH packet. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: ha_pattern: string The pattern is entered as string, the maximum number of entries is 32. Three different characters are permitted. 1 The HARQ ACK is sent (ACK) . Transmission was successful and correct. 0 The NACK is sent (NACK) . Transmission was not correct. With an NACK, the UE requests retransmission of the incorrect data. - Nothing is sent. Transmission is interrupted (Discontinuous Transmission, DTX) ."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:HAPattern?')
		return trim_str_response(response)
