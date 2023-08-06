from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RgPattern:
	"""RgPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rgPattern", core, parent)

	def set(self, rg_pattern: str, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:[HSUPa]:EHICh:RGPAttern \n
		Sets the bit pattern for the ACK/NACK field. \n
			:param rg_pattern: 32-bit long pattern '+' (ACK) and '0' (no signal) For the non serving cell '+' (ACK) and '-' (NACK) For the serving cell
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.value_to_quoted_str(rg_pattern)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSUPa:EHICh:RGPAttern {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:[HSUPa]:EHICh:RGPAttern \n
		Sets the bit pattern for the ACK/NACK field. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: rg_pattern: 32-bit long pattern '+' (ACK) and '0' (no signal) For the non serving cell '+' (ACK) and '-' (NACK) For the serving cell"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSUPa:EHICh:RGPAttern?')
		return trim_str_response(response)
