from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gidh:
	"""Gidh commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gidh", core, parent)

	def set(self, gidh: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:GIDH \n
		Sets GID-H subfield. If the Unsolicited MFB subfield is set to 1, the GID-H subfield contains the highest 3 bits of Group
		ID of the PPDU to which the unsolicited MFB refers. Otherwise this subfield is reserved. \n
			:param gidh: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(gidh)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:GIDH {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:GIDH \n
		Sets GID-H subfield. If the Unsolicited MFB subfield is set to 1, the GID-H subfield contains the highest 3 bits of Group
		ID of the PPDU to which the unsolicited MFB refers. Otherwise this subfield is reserved. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: gidh: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:GIDH?')
		return Conversions.str_to_str_list(response)
