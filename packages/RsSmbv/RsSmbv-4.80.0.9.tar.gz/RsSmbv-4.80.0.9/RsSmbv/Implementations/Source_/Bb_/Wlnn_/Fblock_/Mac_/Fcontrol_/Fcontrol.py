from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fcontrol:
	"""Fcontrol commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fcontrol", core, parent)

	def set(self, fcontrol: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:FCONtrol:FCONtrol \n
		No command help available \n
			:param fcontrol: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(fcontrol)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:FCONtrol:FCONtrol {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:FCONtrol:FCONtrol \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: fcontrol: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:FCONtrol:FCONtrol?')
		return Conversions.str_to_str_list(response)
