from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zpt:
	"""Zpt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zpt", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:[ZPRS<ST>]:ZPT \n
		Sets the parameter subframe configuration period TCSI-RS for CSI-RS with zero transmission power. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Zprs')
			:return: zero_pow_per: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:ZPRS{stream_cmd_val}:ZPT?')
		return Conversions.str_to_str_list(response)
