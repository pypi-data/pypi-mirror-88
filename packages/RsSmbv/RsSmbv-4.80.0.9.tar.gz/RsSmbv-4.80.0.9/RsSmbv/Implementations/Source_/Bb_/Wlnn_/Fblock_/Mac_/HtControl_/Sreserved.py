from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sreserved:
	"""Sreserved commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sreserved", core, parent)

	def set(self, reserved: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:SREServed \n
		This signal field is currently defined, but not used. \n
			:param reserved: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(reserved)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:SREServed {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:SREServed \n
		This signal field is currently defined, but not used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: reserved: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:SREServed?')
		return Conversions.str_to_str_list(response)
