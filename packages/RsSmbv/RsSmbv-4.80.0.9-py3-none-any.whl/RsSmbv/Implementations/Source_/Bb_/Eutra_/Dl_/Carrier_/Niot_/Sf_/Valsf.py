from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Valsf:
	"""Valsf commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("valsf", core, parent)

	def set(self, valid: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:SF<ST>:VALSf \n
		Sets the valid subframes. \n
			:param valid: 0| 1| OFF| ON 1 Valid subframe 0 Not valid subframe
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sf')"""
		param = Conversions.bool_to_str(valid)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:SF{stream_cmd_val}:VALSf {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:SF<ST>:VALSf \n
		Sets the valid subframes. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sf')
			:return: valid: 0| 1| OFF| ON 1 Valid subframe 0 Not valid subframe"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:SF{stream_cmd_val}:VALSf?')
		return Conversions.str_to_bool(response)
