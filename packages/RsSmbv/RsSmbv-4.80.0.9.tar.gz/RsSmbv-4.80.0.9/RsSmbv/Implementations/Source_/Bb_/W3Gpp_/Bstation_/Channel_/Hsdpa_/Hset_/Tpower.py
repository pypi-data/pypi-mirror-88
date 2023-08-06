from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tpower:
	"""Tpower commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tpower", core, parent)

	def set(self, tpower: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:TPOWer \n
		Sets the total power of the HS-PDSCH channels in the H-Set. The individual power levels of the HS-PDSCHs are calculated
		automatically and can be queried with the command method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Power.set. \n
			:param tpower: float The min/max values depend on the number of HS-PDSCH channelization codes (method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Hset.Clength.set) and are calculated as follow: min = -80 dB + 10*log10(NumberOfHS-PDSCHChannelizationCodes) max = 0 dB + 10*log10(NumberOfHS-PDSCHChannelizationCodes) Range: dynamic to dynamic
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(tpower)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:TPOWer {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:TPOWer \n
		Sets the total power of the HS-PDSCH channels in the H-Set. The individual power levels of the HS-PDSCHs are calculated
		automatically and can be queried with the command method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Power.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: tpower: float The min/max values depend on the number of HS-PDSCH channelization codes (method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Hset.Clength.set) and are calculated as follow: min = -80 dB + 10*log10(NumberOfHS-PDSCHChannelizationCodes) max = 0 dB + 10*log10(NumberOfHS-PDSCHChannelizationCodes) Range: dynamic to dynamic"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:TPOWer?')
		return Conversions.str_to_float(response)
