from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CqiType:
	"""CqiType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cqiType", core, parent)

	def set(self, cqi_type: enums.HsMimoCqiType, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:MIMO:TTI<CH>:CQIType \n
		Selects the type of the CQI report. \n
			:param cqi_type: TAST| TADT| TB
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tti')"""
		param = Conversions.enum_scalar_to_str(cqi_type, enums.HsMimoCqiType)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:MIMO:TTI{channel_cmd_val}:CQIType {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.HsMimoCqiType:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:MIMO:TTI<CH>:CQIType \n
		Selects the type of the CQI report. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tti')
			:return: cqi_type: TAST| TADT| TB"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:MIMO:TTI{channel_cmd_val}:CQIType?')
		return Conversions.str_to_scalar_enum(response, enums.HsMimoCqiType)
