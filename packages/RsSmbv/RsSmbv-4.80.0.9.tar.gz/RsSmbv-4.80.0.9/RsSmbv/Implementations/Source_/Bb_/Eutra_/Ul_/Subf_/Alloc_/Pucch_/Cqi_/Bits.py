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

	def set(self, bits: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:CQI:BITS \n
		Sets the number of CQI bits before channel coding. \n
			:param bits: integer Range: 1 to 13
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(bits)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:CQI:BITS {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:CQI:BITS \n
		Sets the number of CQI bits before channel coding. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: bits: integer Range: 1 to 13"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:CQI:BITS?')
		return Conversions.str_to_int(response)
