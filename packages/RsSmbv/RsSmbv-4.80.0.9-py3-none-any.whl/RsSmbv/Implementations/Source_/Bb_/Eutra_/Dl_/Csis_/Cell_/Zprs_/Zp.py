from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zp:
	"""Zp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zp", core, parent)

	def set(self, zero_pow: List[str], channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:[ZPRS<ST>]:ZP \n
		Sets the used CSI-RS configurations in the zero transmission power subframes. \n
			:param zero_pow: decimal value In the user interface, the 16 bits are set as a hexadecimal value. In the remote control, as a decimal value. Range: 0 to 65535
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Zprs')"""
		param = Conversions.list_to_csv_str(zero_pow)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:ZPRS{stream_cmd_val}:ZP {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:[ZPRS<ST>]:ZP \n
		Sets the used CSI-RS configurations in the zero transmission power subframes. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Zprs')
			:return: zero_pow: decimal value In the user interface, the 16 bits are set as a hexadecimal value. In the remote control, as a decimal value. Range: 0 to 65535"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:ZPRS{stream_cmd_val}:ZP?')
		return Conversions.str_to_str_list(response)
