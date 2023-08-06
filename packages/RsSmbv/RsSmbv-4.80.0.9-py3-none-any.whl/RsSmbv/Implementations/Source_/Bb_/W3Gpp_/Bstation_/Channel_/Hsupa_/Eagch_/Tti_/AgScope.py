from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AgScope:
	"""AgScope commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("agScope", core, parent)

	def set(self, ag_scocpe: enums.HsUpaAgchScope, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:[HSUPa]:EAGCh:TTI<DI>:AGSCope \n
		Sets the scope of the selected grant. According to the TS 25.321, the impact of each grant on the UE depends on this
		parameter. For E-DCH TTI = 10ms, the absolute grant scope is always ALL (All HARQ Processes) . \n
			:param ag_scocpe: ALL| PER
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tti')"""
		param = Conversions.enum_scalar_to_str(ag_scocpe, enums.HsUpaAgchScope)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSUPa:EAGCh:TTI{twoStreams_cmd_val}:AGSCope {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> enums.HsUpaAgchScope:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:[HSUPa]:EAGCh:TTI<DI>:AGSCope \n
		Sets the scope of the selected grant. According to the TS 25.321, the impact of each grant on the UE depends on this
		parameter. For E-DCH TTI = 10ms, the absolute grant scope is always ALL (All HARQ Processes) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tti')
			:return: ag_scocpe: ALL| PER"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSUPa:EAGCh:TTI{twoStreams_cmd_val}:AGSCope?')
		return Conversions.str_to_scalar_enum(response, enums.HsUpaAgchScope)
