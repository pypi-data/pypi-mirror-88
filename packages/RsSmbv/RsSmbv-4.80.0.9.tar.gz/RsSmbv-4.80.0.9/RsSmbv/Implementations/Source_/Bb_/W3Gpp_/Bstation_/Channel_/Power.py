from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def set(self, power: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:POWer \n
		Sets the channel power relative to the powers of the other channels. This setting also determines the starting power of
		the channel for Misuse TPC, Dynamic Power Control and the power control sequence simulation of OCNS mode 3i channels.
		With the command method RsSmbv.Source.Bb.W3Gpp.Power.Adjust.set, the power of all the activated channels is adapted so
		that the total power corresponds to 0 dB. This does not change the power ratio among the individual channels. \n
			:param power: float Range: -80 to 0
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(power)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:POWer {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:POWer \n
		Sets the channel power relative to the powers of the other channels. This setting also determines the starting power of
		the channel for Misuse TPC, Dynamic Power Control and the power control sequence simulation of OCNS mode 3i channels.
		With the command method RsSmbv.Source.Bb.W3Gpp.Power.Adjust.set, the power of all the activated channels is adapted so
		that the total power corresponds to 0 dB. This does not change the power ratio among the individual channels. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: power: float Range: -80 to 0"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:POWer?')
		return Conversions.str_to_float(response)
