from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.TdscdmaChanType, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:CHANnel<US>:TYPE \n
		Sets the channel type. In the uplink, the channel type is fixed for channel number 0. In the downlink, the channel type
		is fixed for channel numbers 0 to 5. For the remaining numbers, the choice lies between the relevant standard channels
		and the high speed channels. \n
			:param type_py: P_CCPCH1| P_CCPCH2| S_CCPCH1| S_CCPCH2| FPACH| PDSCH| DPCH_QPSQ| DPCH_8PSQ| HS_SCCH1| HS_SCCH2| HS_PDS_QPSK| HS_PDS_16QAM| PUSCH| UP_DPCH_QPSK| UP_DPCH_8PSK| HS_SICH| HS_PDS_64QAM| E_PUCH_QPSK| E_PUCH_16QAM| E_RUCCH| PLCCH| EAGCH| EHICH
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.TdscdmaChanType)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> enums.TdscdmaChanType:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:CHANnel<US>:TYPE \n
		Sets the channel type. In the uplink, the channel type is fixed for channel number 0. In the downlink, the channel type
		is fixed for channel numbers 0 to 5. For the remaining numbers, the choice lies between the relevant standard channels
		and the high speed channels. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: type_py: P_CCPCH1| P_CCPCH2| S_CCPCH1| S_CCPCH2| FPACH| PDSCH| DPCH_QPSQ| DPCH_8PSQ| HS_SCCH1| HS_SCCH2| HS_PDS_QPSK| HS_PDS_16QAM| PUSCH| UP_DPCH_QPSK| UP_DPCH_8PSK| HS_SICH| HS_PDS_64QAM| E_PUCH_QPSK| E_PUCH_16QAM| E_RUCCH| PLCCH| EAGCH| EHICH"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaChanType)
