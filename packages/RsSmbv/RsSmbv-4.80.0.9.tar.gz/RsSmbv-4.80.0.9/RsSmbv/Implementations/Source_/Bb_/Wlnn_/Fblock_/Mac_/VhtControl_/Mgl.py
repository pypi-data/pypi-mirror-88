from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mgl:
	"""Mgl commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mgl", core, parent)

	def set(self, mfsi_gid_l: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MGL \n
		The command determines the information of the MFSI/GID-L subfield. MFB = 0 If the Unsolicited MFB subfield is set to 0,
		the MFSI/GID-L subfield contains the received value of MSI contained in the frame to which the MFB information refers.
		MFB = 1 The MFSI/GID-L subfield contains the lowest 3 bits of Group ID of the PPDU to which the unsolicited MFB refers. \n
			:param mfsi_gid_l: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(mfsi_gid_l)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:MGL {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MGL \n
		The command determines the information of the MFSI/GID-L subfield. MFB = 0 If the Unsolicited MFB subfield is set to 0,
		the MFSI/GID-L subfield contains the received value of MSI contained in the frame to which the MFB information refers.
		MFB = 1 The MFSI/GID-L subfield contains the lowest 3 bits of Group ID of the PPDU to which the unsolicited MFB refers. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: mfsi_gid_l: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:MGL?')
		return Conversions.str_to_str_list(response)
