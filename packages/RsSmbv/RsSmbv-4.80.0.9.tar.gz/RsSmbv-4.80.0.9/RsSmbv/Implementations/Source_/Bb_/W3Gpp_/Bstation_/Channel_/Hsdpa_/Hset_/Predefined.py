from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Predefined:
	"""Predefined commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("predefined", core, parent)

	def set(self, predefined: enums.HsHsetType, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:PREDefined \n
		The command selects the H-Set and the modulation according to TS 25.101 Annex A.7. \n
			:param predefined: P1QPSK| P1QAM16| P2QPSK| P2QAM16| P3QPSK| P3QAM16| P4QPSK| P5QPSK| P6QPSK| P6QAM16| P7QPSK| P8QAM64| P9QAM16QPSK| P10QPSK| P10QAM16| P11QAM64QAM16| P12QPSK| USER
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(predefined, enums.HsHsetType)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:PREDefined {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.HsHsetType:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:PREDefined \n
		The command selects the H-Set and the modulation according to TS 25.101 Annex A.7. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: predefined: P1QPSK| P1QAM16| P2QPSK| P2QAM16| P3QPSK| P3QAM16| P4QPSK| P5QPSK| P6QPSK| P6QAM16| P7QPSK| P8QAM64| P9QAM16QPSK| P10QPSK| P10QAM16| P11QAM64QAM16| P12QPSK| USER"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:PREDefined?')
		return Conversions.str_to_scalar_enum(response, enums.HsHsetType)
