from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mfb:
	"""Mfb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mfb", core, parent)

	def set(self, mfb: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MFB \n
		The command sets the MFB subfield. This subfield contains the recommended MFB. The value of MCS=15 and VHT N_STS=7
		indicates that no feedback is present. See also Table 'MFB subfield in the VHT format HT control field' for definition of
		the MFB subfield. \n
			:param mfb: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(mfb)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:MFB {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MFB \n
		The command sets the MFB subfield. This subfield contains the recommended MFB. The value of MCS=15 and VHT N_STS=7
		indicates that no feedback is present. See also Table 'MFB subfield in the VHT format HT control field' for definition of
		the MFB subfield. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: mfb: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:MFB?')
		return Conversions.str_to_str_list(response)
