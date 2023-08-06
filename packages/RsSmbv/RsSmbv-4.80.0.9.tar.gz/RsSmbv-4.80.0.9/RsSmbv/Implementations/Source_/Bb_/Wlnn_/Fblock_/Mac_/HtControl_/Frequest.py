from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequest:
	"""Frequest commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequest", core, parent)

	def set(self, frequest: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:FREQuest \n
		Sets the value for the feedback request. 00 = no request 01 = unsolicited feedback only 10 = immediate feedback 11 =
		aggregated feedback \n
			:param frequest: integer Range: #H0,2 to #H3,2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(frequest)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:FREQuest {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:FREQuest \n
		Sets the value for the feedback request. 00 = no request 01 = unsolicited feedback only 10 = immediate feedback 11 =
		aggregated feedback \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: frequest: integer Range: #H0,2 to #H3,2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:FREQuest?')
		return Conversions.str_to_str_list(response)
