from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, sar_mode: enums.SarMode, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:NMESsage:INAV:EPHemeris:SAR:MODE \n
		Sets the Search-and-Rescue Service (SAR) mode for SAR message generation. SAR messages are specified by the 22-bit SAR
		field in the I/NAV navigation message. For more information, refer to specification . \n
			:param sar_mode: SPARe| SRLM| LRLM SPARe Generates spare SAR data. The start bit is set to one. SAR receivers interpret the following 21 spare bits as SAR non-relevant data. SRLM/LRLM Generates SAR data for nominal mode operation in the Galileo E1-B component. For the SAR message format, you can select between short return link message (SRLM) and long return link message (LRLM) . For the real navigation message, the Short/Long RLM Identifier, in the SAR data field is set accordingly (0 = Short RLM, 1 = Long RLM) .
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.enum_scalar_to_str(sar_mode, enums.SarMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:NMESsage:INAV:EPHemeris:SAR:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.SarMode:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo<ST>:NMESsage:INAV:EPHemeris:SAR:MODE \n
		Sets the Search-and-Rescue Service (SAR) mode for SAR message generation. SAR messages are specified by the 22-bit SAR
		field in the I/NAV navigation message. For more information, refer to specification . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: sar_mode: SPARe| SRLM| LRLM SPARe Generates spare SAR data. The start bit is set to one. SAR receivers interpret the following 21 spare bits as SAR non-relevant data. SRLM/LRLM Generates SAR data for nominal mode operation in the Galileo E1-B component. For the SAR message format, you can select between short return link message (SRLM) and long return link message (LRLM) . For the real navigation message, the Short/Long RLM Identifier, in the SAR data field is set accordingly (0 = Short RLM, 1 = Long RLM) ."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GALileo{stream_cmd_val}:NMESsage:INAV:EPHemeris:SAR:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SarMode)
