from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.HsMode, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:MODE \n
		The command selects the HSDPA mode. \n
			:param mode: CONTinuous| PSF0| PSF1| PSF2| PSF3| PSF4| HSET CONTinuous The high speed channel is generated continuously. This mode is defined in test model 5. PSFx The high speed channel is generated in packet mode. The start of the channel is set by selecting the subframe in which the first packet is sent. HSET The high speed channels are preset according to TS 25.1401 Annex A.7, H-Set.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(mode, enums.HsMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.HsMode:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:MODE \n
		The command selects the HSDPA mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: mode: CONTinuous| PSF0| PSF1| PSF2| PSF3| PSF4| HSET CONTinuous The high speed channel is generated continuously. This mode is defined in test model 5. PSFx The high speed channel is generated in packet mode. The start of the channel is set by selecting the subframe in which the first packet is sent. HSET The high speed channels are preset according to TS 25.1401 Annex A.7, H-Set."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.HsMode)
