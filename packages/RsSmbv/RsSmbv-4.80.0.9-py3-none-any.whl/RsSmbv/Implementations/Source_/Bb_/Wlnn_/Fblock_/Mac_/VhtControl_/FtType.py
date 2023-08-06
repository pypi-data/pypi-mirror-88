from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FtType:
	"""FtType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ftType", core, parent)

	def set(self, fb_tx_type: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:FTTYpe \n
		The command sets the FB Tx Type subfield. 0 = If the Unsolicited MFB subfield is set to 1 and FB Tx Type subfield is set
		to 0, the unsolicited MFB refers to either an unbeamformed VHT PPDU or transmit diversity using an STBC VHT PPDU. 1 = If
		the Unsolicited MFB subfield is set to 1 and the FB Tx Type subfield is set to 1, the unsolicited MFB refers to a
		beamformed SU-MIMO VHT PPDU. Otherwise this subfield is reserved. \n
			:param fb_tx_type: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(fb_tx_type)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:FTTYpe {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:FTTYpe \n
		The command sets the FB Tx Type subfield. 0 = If the Unsolicited MFB subfield is set to 1 and FB Tx Type subfield is set
		to 0, the unsolicited MFB refers to either an unbeamformed VHT PPDU or transmit diversity using an STBC VHT PPDU. 1 = If
		the Unsolicited MFB subfield is set to 1 and the FB Tx Type subfield is set to 1, the unsolicited MFB refers to a
		beamformed SU-MIMO VHT PPDU. Otherwise this subfield is reserved. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: fb_tx_type: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:FTTYpe?')
		return Conversions.str_to_str_list(response)
