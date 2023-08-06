from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RvIndex:
	"""RvIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rvIndex", core, parent)

	def set(self, redund_vers_index: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:CCODing:RVINdex \n
		Sets the redundancy version index. \n
			:param redund_vers_index: integer Range: 0 to 3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')"""
		param = Conversions.decimal_value_to_str(redund_vers_index)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:CCODing:RVINdex {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:CCODing:RVINdex \n
		Sets the redundancy version index. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')
			:return: redund_vers_index: integer Range: 0 to 3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:CCODing:RVINdex?')
		return Conversions.str_to_int(response)
