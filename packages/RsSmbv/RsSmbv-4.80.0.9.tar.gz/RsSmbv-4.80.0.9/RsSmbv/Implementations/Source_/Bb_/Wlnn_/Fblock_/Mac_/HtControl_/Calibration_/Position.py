from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Position:
	"""Position commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("position", core, parent)

	def set(self, position: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:CALibration:POSition \n
		Sets the value for the calibration position. 00 = Not a calibration frame (Default setting) 01 = Calibration Start 10 =
		Sounding Response 11 = Sounding Complete \n
			:param position: integer Range: #H0,2 to #H3,2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(position)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:CALibration:POSition {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:CALibration:POSition \n
		Sets the value for the calibration position. 00 = Not a calibration frame (Default setting) 01 = Calibration Start 10 =
		Sounding Response 11 = Sounding Complete \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: position: integer Range: #H0,2 to #H3,2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:CALibration:POSition?')
		return Conversions.str_to_str_list(response)
