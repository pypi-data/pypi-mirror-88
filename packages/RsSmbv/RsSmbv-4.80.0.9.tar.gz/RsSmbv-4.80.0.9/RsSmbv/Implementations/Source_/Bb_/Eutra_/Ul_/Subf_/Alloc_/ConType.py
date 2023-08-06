from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConType:
	"""ConType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("conType", core, parent)

	def set(self, content_type: enums.EutraUlContentTypeWithIot, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:CONType \n
		Selects the content type for the selected allocation. \n
			:param content_type: PUSCh| PUCCh | EMTC| NIOT
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(content_type, enums.EutraUlContentTypeWithIot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CONType {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraUlContentTypeWithIot:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:CONType \n
		Selects the content type for the selected allocation. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: content_type: PUSCh| PUCCh | EMTC| NIOT"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CONType?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUlContentTypeWithIot)
