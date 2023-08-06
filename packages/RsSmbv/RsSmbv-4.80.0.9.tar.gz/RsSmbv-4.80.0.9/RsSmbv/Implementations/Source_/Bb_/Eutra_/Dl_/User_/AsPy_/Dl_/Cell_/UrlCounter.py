from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UrlCounter:
	"""UrlCounter commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("urlCounter", core, parent)

	def set(self, use_rlc_counter: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:URLCounter \n
		Enables/disables the use of RLC counter. \n
			:param use_rlc_counter: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		param = Conversions.bool_to_str(use_rlc_counter)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:URLCounter {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:URLCounter \n
		Enables/disables the use of RLC counter. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1
			:return: use_rlc_counter: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:URLCounter?')
		return Conversions.str_to_bool(response)
