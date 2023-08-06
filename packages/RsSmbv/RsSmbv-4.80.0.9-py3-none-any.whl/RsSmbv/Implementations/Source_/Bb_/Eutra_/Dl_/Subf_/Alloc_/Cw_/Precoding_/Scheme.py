from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scheme:
	"""Scheme commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scheme", core, parent)

	def set(self, scheme: enums.EutraDlpRecMultAntScheme, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:PRECoding:SCHeme \n
		(available for the first codeword only) Selects the precoding scheme. The available selections depend on the selected
		content type. \n
			:param scheme: NONE| SPM| TXD| BF NONE Disables precoding. SPM Spatial multiplexing TXD Transmit diversity BF Sets the PDSCH to transmission mode selected with the command BB:EUTRa:PRECoding:TRSCheme.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')"""
		param = Conversions.enum_scalar_to_str(scheme, enums.EutraDlpRecMultAntScheme)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:PRECoding:SCHeme {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> enums.EutraDlpRecMultAntScheme:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:PRECoding:SCHeme \n
		(available for the first codeword only) Selects the precoding scheme. The available selections depend on the selected
		content type. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')
			:return: scheme: NONE| SPM| TXD| BF NONE Disables precoding. SPM Spatial multiplexing TXD Transmit diversity BF Sets the PDSCH to transmission mode selected with the command BB:EUTRa:PRECoding:TRSCheme."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:PRECoding:SCHeme?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDlpRecMultAntScheme)
