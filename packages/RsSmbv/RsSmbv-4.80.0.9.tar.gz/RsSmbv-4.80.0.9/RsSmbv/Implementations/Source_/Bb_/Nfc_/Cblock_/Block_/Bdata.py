from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bdata:
	"""Bdata commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bdata", core, parent)

	def set(self, bdata: List[str], channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:BDATa \n
		Sets the value of 'Block Data' . \n
			:param bdata: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')"""
		param = Conversions.list_to_csv_str(bdata)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BLOCk{stream_cmd_val}:BDATa {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:BDATa \n
		Sets the value of 'Block Data' . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
			:return: bdata: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BLOCk{stream_cmd_val}:BDATa?')
		return Conversions.str_to_str_list(response)
