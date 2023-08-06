from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Read:
	"""Read commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("read", core, parent)

	def set(self, read: enums.TpcReadMode, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:SLOT<CH>:CHANnel<US>:DPCCh:TPC:READ \n
		Sets the read out mode for the bit pattern of the TPC field. \n
			:param read: CONTinuous| S0A| S1A| S01A| S10A CONTinous The TPC bits are used cyclically. S0A The TPC bits are used once and then the TPC sequence is continued with 0 bits. S1A The TPC bits are used once and then the TPC sequence is continued with 1 bit. S01A The TPC bits are used once and then the TPC sequence is continued with 0 and 1 bits alternately S10A The TPC bits are used once, and then the TPC sequence is continued with 1 and 0 bits alternately
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(read, enums.TpcReadMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:DPCCh:TPC:READ {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> enums.TpcReadMode:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:SLOT<CH>:CHANnel<US>:DPCCh:TPC:READ \n
		Sets the read out mode for the bit pattern of the TPC field. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: read: CONTinuous| S0A| S1A| S01A| S10A CONTinous The TPC bits are used cyclically. S0A The TPC bits are used once and then the TPC sequence is continued with 0 bits. S1A The TPC bits are used once and then the TPC sequence is continued with 1 bit. S01A The TPC bits are used once and then the TPC sequence is continued with 0 and 1 bits alternately S10A The TPC bits are used once, and then the TPC sequence is continued with 1 and 0 bits alternately"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:DPCCh:TPC:READ?')
		return Conversions.str_to_scalar_enum(response, enums.TpcReadMode)
