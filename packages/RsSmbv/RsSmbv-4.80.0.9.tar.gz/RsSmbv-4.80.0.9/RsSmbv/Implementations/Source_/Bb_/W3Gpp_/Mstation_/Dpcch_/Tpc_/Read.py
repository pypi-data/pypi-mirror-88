from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Read:
	"""Read commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("read", core, parent)

	def set(self, read: enums.TpcReadMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:TPC:READ \n
		The command sets the read out mode for the bit pattern of the TPC field of the DPCCH. The bit pattern is selected with
		the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tpc.Data.Pattern.set. \n
			:param read: CONTinuous| S0A| S1A| S01A| S10A CONTinuous The bit pattern is used cyclically. S0A The bit pattern is used once, then the TPC sequence continues with 0 bits. S1A The bit pattern is used once, then the TPC sequence continues with 1 bit. S01A The bit pattern is used once and then the TPC sequence is continued with 0 bits and 1 bit alternately (in multiples, depending on by the symbol rate, for example, 00001111) . S10A The bit pattern is used once and then the TPC sequence is continued with 1 bit and 0 bits alternately (in multiples, depending on by the symbol rate, for example, 11110000) .
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(read, enums.TpcReadMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:TPC:READ {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TpcReadMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:TPC:READ \n
		The command sets the read out mode for the bit pattern of the TPC field of the DPCCH. The bit pattern is selected with
		the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tpc.Data.Pattern.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: read: CONTinuous| S0A| S1A| S01A| S10A CONTinuous The bit pattern is used cyclically. S0A The bit pattern is used once, then the TPC sequence continues with 0 bits. S1A The bit pattern is used once, then the TPC sequence continues with 1 bit. S01A The bit pattern is used once and then the TPC sequence is continued with 0 bits and 1 bit alternately (in multiples, depending on by the symbol rate, for example, 00001111) . S10A The bit pattern is used once and then the TPC sequence is continued with 1 bit and 0 bits alternately (in multiples, depending on by the symbol rate, for example, 11110000) ."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:TPC:READ?')
		return Conversions.str_to_scalar_enum(response, enums.TpcReadMode)
