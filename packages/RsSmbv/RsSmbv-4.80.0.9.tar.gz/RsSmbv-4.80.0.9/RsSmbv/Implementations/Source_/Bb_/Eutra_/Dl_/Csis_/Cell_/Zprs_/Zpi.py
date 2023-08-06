from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zpi:
	"""Zpi commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zpi", core, parent)

	def set(self, zero_pow_conf: List[str], channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:[ZPRS<ST>]:ZPI \n
		Sets the parameter ICSI-RS for CSI-RS with zero transmission power. \n
			:param zero_pow_conf: integer Range: 0 to 154
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Zprs')"""
		param = Conversions.list_to_csv_str(zero_pow_conf)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:ZPRS{stream_cmd_val}:ZPI {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:[ZPRS<ST>]:ZPI \n
		Sets the parameter ICSI-RS for CSI-RS with zero transmission power. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Zprs')
			:return: zero_pow_conf: integer Range: 0 to 154"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:ZPRS{stream_cmd_val}:ZPI?')
		return Conversions.str_to_str_list(response)
