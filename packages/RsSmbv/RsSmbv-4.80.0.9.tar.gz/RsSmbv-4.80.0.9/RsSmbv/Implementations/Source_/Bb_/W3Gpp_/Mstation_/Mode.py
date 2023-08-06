from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.MsMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:MODE \n
		The command selects the operating mode for the user equipment. \n
			:param mode: PRACh| PCPCh| DPCDch| PPRach| PPCPch PRACh The user equipment only generates a signal with a physical random access channel (PRACH) . This channel is used to set up the user equipment connection with the base station. The channel-specific parameters of the PRACH can be set with the commands :SOURce:BB:W3GPp:MSTationn:PRACh:.... PPRAch The user equipment only generates a signal with the preamble component of a physical random access channel (PRACH) . The parameters of the PRACH preamble can be set with the commands :SOURce:BB:W3GPp:MSTationn:PRACh:.... PCPCh The user equipment only generates a signal with a physical common packet channel (PCPCH) . This channel is used to transmit packet-oriented services (e.g. SMS) . The channel-specific parameters of the PCPCH can be set with the commands :SOURce:BB:W3GPp:MSTationn:PCPCh:.... PPCPch The user equipment only generates a signal with the preamble component of a physical common packet channel (PCPCH) . The parameters of the PCPCH preamble can be set with the commands :SOURce:BB:W3GPp:MSTationn:PCPCh:.... DPCDch The user equipment generates a signal with a dedicated physical control channel (DPCCH) , up to 6 dedicated physical data channels (DPDCH) , up to one HS-DPCCH channel, up to one E-DPCCH channel and up to four E-DPDCH channels. This signal is used for voice and data transmission.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(mode, enums.MsMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.MsMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:MODE \n
		The command selects the operating mode for the user equipment. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: mode: PRACh| PCPCh| DPCDch| PPRach| PPCPch PRACh The user equipment only generates a signal with a physical random access channel (PRACH) . This channel is used to set up the user equipment connection with the base station. The channel-specific parameters of the PRACH can be set with the commands :SOURce:BB:W3GPp:MSTationn:PRACh:.... PPRAch The user equipment only generates a signal with the preamble component of a physical random access channel (PRACH) . The parameters of the PRACH preamble can be set with the commands :SOURce:BB:W3GPp:MSTationn:PRACh:.... PCPCh The user equipment only generates a signal with a physical common packet channel (PCPCH) . This channel is used to transmit packet-oriented services (e.g. SMS) . The channel-specific parameters of the PCPCH can be set with the commands :SOURce:BB:W3GPp:MSTationn:PCPCh:.... PPCPch The user equipment only generates a signal with the preamble component of a physical common packet channel (PCPCH) . The parameters of the PCPCH preamble can be set with the commands :SOURce:BB:W3GPp:MSTationn:PCPCh:.... DPCDch The user equipment generates a signal with a dedicated physical control channel (DPCCH) , up to 6 dedicated physical data channels (DPDCH) , up to one HS-DPCCH channel, up to one E-DPCCH channel and up to four E-DPDCH channels. This signal is used for voice and data transmission."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MsMode)
