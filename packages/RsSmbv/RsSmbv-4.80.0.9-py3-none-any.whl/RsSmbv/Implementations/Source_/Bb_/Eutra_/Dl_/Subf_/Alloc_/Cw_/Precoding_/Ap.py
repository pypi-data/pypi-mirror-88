from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ap:
	"""Ap commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ap", core, parent)

	def set(self, antenna_ports: enums.EutraBfaNtSet, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:PRECoding:AP \n
		Sets the antenna port(s) for the selected transmission mode. \n
			:param antenna_ports: AP7| AP5| AP8| AP78| AP79| AP710| AP711| AP712| AP713| AP714| AP107| AP108| AP109| AP110| AP107108| AP107109| AP11| AP13| AP1113 | AP7| AP5| AP8| AP78| AP79| AP710| AP711| AP712| AP713| AP714 | AP11| AP13| AP1113| AP107| AP108| AP109| AP110| AP107108| AP107109 Antenna port or antenna ports combination; the designation AP78 for example means AP7 and AP8
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')"""
		param = Conversions.enum_scalar_to_str(antenna_ports, enums.EutraBfaNtSet)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:PRECoding:AP {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> enums.EutraBfaNtSet:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:PRECoding:AP \n
		Sets the antenna port(s) for the selected transmission mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')
			:return: antenna_ports: AP7| AP5| AP8| AP78| AP79| AP710| AP711| AP712| AP713| AP714| AP107| AP108| AP109| AP110| AP107108| AP107109| AP11| AP13| AP1113 | AP7| AP5| AP8| AP78| AP79| AP710| AP711| AP712| AP713| AP714 | AP11| AP13| AP1113| AP107| AP108| AP109| AP110| AP107108| AP107109 Antenna port or antenna ports combination; the designation AP78 for example means AP7 and AP8"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:PRECoding:AP?')
		return Conversions.str_to_scalar_enum(response, enums.EutraBfaNtSet)
