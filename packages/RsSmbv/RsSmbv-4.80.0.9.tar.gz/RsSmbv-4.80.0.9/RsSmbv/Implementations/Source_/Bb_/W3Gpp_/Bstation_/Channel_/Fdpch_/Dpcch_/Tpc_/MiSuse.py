from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MiSuse:
	"""MiSuse commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("miSuse", core, parent)

	def set(self, misuse: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:FDPCh:DPCCh:TPC:MISuse \n
		The command activates 'mis-' use of the TPC field (Transmit Power Control) of the selected channel for controlling the
		channel powers of these channels of the specified base station. The bit pattern (see command method RsSmbv.Source.Bb.
		W3Gpp.Bstation.Channel.Fdpch.Dpcch.Tpc.Data.Pattern.set) of the TPC field of each channel is used to control the channel
		power. A '1' leads to an increase of channel powers, a '0' to a reduction of channel powers. Channel power is limited to
		the range 0 dB to -60 dB. The step width of the change is defined with the command method RsSmbv.Source.Bb.W3Gpp.Bstation.
		Channel.Fdpch.Dpcch.Tpc.Pstep.set. \n
			:param misuse: ON| OFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(misuse)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:FDPCh:DPCCh:TPC:MISuse {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:FDPCh:DPCCh:TPC:MISuse \n
		The command activates 'mis-' use of the TPC field (Transmit Power Control) of the selected channel for controlling the
		channel powers of these channels of the specified base station. The bit pattern (see command method RsSmbv.Source.Bb.
		W3Gpp.Bstation.Channel.Fdpch.Dpcch.Tpc.Data.Pattern.set) of the TPC field of each channel is used to control the channel
		power. A '1' leads to an increase of channel powers, a '0' to a reduction of channel powers. Channel power is limited to
		the range 0 dB to -60 dB. The step width of the change is defined with the command method RsSmbv.Source.Bb.W3Gpp.Bstation.
		Channel.Fdpch.Dpcch.Tpc.Pstep.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: misuse: ON| OFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:FDPCh:DPCCh:TPC:MISuse?')
		return Conversions.str_to_bool(response)
