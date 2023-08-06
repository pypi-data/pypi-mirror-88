from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ueid:
	"""Ueid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ueid", core, parent)

	def set(self, ueid: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:[HSUPa]:EAGCh:TTI<DI>:UEID \n
		Sets the UE Id for the selected TTI. \n
			:param ueid: integer Range: 0 to 65535
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tti')"""
		param = Conversions.decimal_value_to_str(ueid)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSUPa:EAGCh:TTI{twoStreams_cmd_val}:UEID {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:[HSUPa]:EAGCh:TTI<DI>:UEID \n
		Sets the UE Id for the selected TTI. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tti')
			:return: ueid: integer Range: 0 to 65535"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSUPa:EAGCh:TTI{twoStreams_cmd_val}:UEID?')
		return Conversions.str_to_int(response)
