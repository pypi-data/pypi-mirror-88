from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Altmodulation:
	"""Altmodulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("altmodulation", core, parent)

	def set(self, alt_modulation: enums.ModulationC, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:ALTModulation \n
		Sets the alternative modulation (see 'Randomly Varying Modulation and Number of Codes (Type 3i) Settings') . \n
			:param alt_modulation: QPSK| QAM16| QAM64
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(alt_modulation, enums.ModulationC)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:ALTModulation {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.ModulationC:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:ALTModulation \n
		Sets the alternative modulation (see 'Randomly Varying Modulation and Number of Codes (Type 3i) Settings') . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: alt_modulation: QPSK| QAM16| QAM64"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:ALTModulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationC)
