from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hacbook:
	"""Hacbook commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hacbook", core, parent)

	def set(self, harq_ack_codebook: enums.AllHarqAckCodebook, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SYINfo:HACBook \n
		Defines the HARQ ACK reporting according to the PDSCH HARQ ACK codebook. \n
			:param harq_ack_codebook: SEMistatic| DYNamic SEMistatic Sets the HARQ ACK reporting according to the PDSCH HARQ ACK codebook to 'Semi-static'. A UE reports HARQ ACK information for a corresponding PDSCH reception or SPS PDSCH release only in a HARQ ACK codebook that the UE transmits in a slot indicated by a value of a PDSCH-to- HARQ feedback timing indicator field in a corresponding DCI format 1_0 or DCI format 1_1. The UE reports NACK values for HARQ-ACK information bits in an HARQ-ACK codebook that the UE transmits in a slot not indicated by a value of a PDSCH-to-HARQ feedback timing indicator field in a corresponding DCI format 1_0 or DCI format 1_1. DYNamic Sets the HARQ ACK reporting according to the PDSCH HARQ ACK codebook to 'dynamic'. For a serving cell, an active DL BWP, and an active UL BWP, as described in clause 12, the UE determines a set of occasions for candidate PDSCH receptions for which the UE can transmit corresponding HARQ ACK information in a PUCCH in slot . If serving cell is deactivated, the UE uses as the active DL BWP for determining the set of occasions for candidate PDSCH receptions a DL BWP provided by firstActiveDownlinkBWP-ID.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(harq_ack_codebook, enums.AllHarqAckCodebook)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SYINfo:HACBook {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.AllHarqAckCodebook:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SYINfo:HACBook \n
		Defines the HARQ ACK reporting according to the PDSCH HARQ ACK codebook. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: harq_ack_codebook: SEMistatic| DYNamic SEMistatic Sets the HARQ ACK reporting according to the PDSCH HARQ ACK codebook to 'Semi-static'. A UE reports HARQ ACK information for a corresponding PDSCH reception or SPS PDSCH release only in a HARQ ACK codebook that the UE transmits in a slot indicated by a value of a PDSCH-to- HARQ feedback timing indicator field in a corresponding DCI format 1_0 or DCI format 1_1. The UE reports NACK values for HARQ-ACK information bits in an HARQ-ACK codebook that the UE transmits in a slot not indicated by a value of a PDSCH-to-HARQ feedback timing indicator field in a corresponding DCI format 1_0 or DCI format 1_1. DYNamic Sets the HARQ ACK reporting according to the PDSCH HARQ ACK codebook to 'dynamic'. For a serving cell, an active DL BWP, and an active UL BWP, as described in clause 12, the UE determines a set of occasions for candidate PDSCH receptions for which the UE can transmit corresponding HARQ ACK information in a PUCCH in slot . If serving cell is deactivated, the UE uses as the active DL BWP for determining the set of occasions for candidate PDSCH receptions a DL BWP provided by firstActiveDownlinkBWP-ID."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SYINfo:HACBook?')
		return Conversions.str_to_scalar_enum(response, enums.AllHarqAckCodebook)
