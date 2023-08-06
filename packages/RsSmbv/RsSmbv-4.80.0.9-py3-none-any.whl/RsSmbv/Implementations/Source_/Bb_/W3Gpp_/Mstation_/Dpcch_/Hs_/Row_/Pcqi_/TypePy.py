from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, cqi_type: enums.HsRel8CqiType, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:PCQI<DI>:TYPE \n
		Selects the type of the PCI/CQI report. \n
			:param cqi_type: DTX| CQI| TAST| TADT| TB| CCQI TAST|TADT Type A Single TB, Type A Double TB TB Type B CCQI Composite CQI
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Pcqi')"""
		param = Conversions.enum_scalar_to_str(cqi_type, enums.HsRel8CqiType)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:PCQI{twoStreams_cmd_val}:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> enums.HsRel8CqiType:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:PCQI<DI>:TYPE \n
		Selects the type of the PCI/CQI report. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Pcqi')
			:return: cqi_type: DTX| CQI| TAST| TADT| TB| CCQI TAST|TADT Type A Single TB, Type A Double TB TB Type B CCQI Composite CQI"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:PCQI{twoStreams_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.HsRel8CqiType)
