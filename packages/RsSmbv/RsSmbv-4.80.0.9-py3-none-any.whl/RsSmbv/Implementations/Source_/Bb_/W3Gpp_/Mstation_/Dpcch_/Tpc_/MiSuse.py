from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MiSuse:
	"""MiSuse commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("miSuse", core, parent)

	def set(self, mis_use: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:TPC:MISuse \n
		The command activates 'mis-' use of the TPC field (Transmit Power Control) for controlling the channel power of the user
		equipment. The bit pattern (see commands :SOURce:BB:W3GPp:MSTation:DPCCh:TPC:DATA...) of the TPC field of the DPCCH is
		used to control the channel power. A '1' leads to an increase of channel powers, a '0' to a reduction of channel powers.
		Channel power is limited to the range 0 dB to -60 dB. The step width for the change is defined by the command method
		RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tpc.Pstep.set. Note: 'Mis-'using the TPC field is available for UE2, UE3,UE4 only. \n
			:param mis_use: ON| OFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.bool_to_str(mis_use)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:TPC:MISuse {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:TPC:MISuse \n
		The command activates 'mis-' use of the TPC field (Transmit Power Control) for controlling the channel power of the user
		equipment. The bit pattern (see commands :SOURce:BB:W3GPp:MSTation:DPCCh:TPC:DATA...) of the TPC field of the DPCCH is
		used to control the channel power. A '1' leads to an increase of channel powers, a '0' to a reduction of channel powers.
		Channel power is limited to the range 0 dB to -60 dB. The step width for the change is defined by the command method
		RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tpc.Pstep.set. Note: 'Mis-'using the TPC field is available for UE2, UE3,UE4 only. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: mis_use: ON| OFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:TPC:MISuse?')
		return Conversions.str_to_bool(response)
