from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Msi:
	"""Msi commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("msi", core, parent)

	def set(self, msi: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MSI \n
		The command sets the MSI subfield. MRQ = 0 When the MRQ subfield is set to 0, the MSI subfield is reserved. MRQ = 1 When
		the MRQ subfield is set to 1, the MSI subfield contains a sequence number in the range 0 to 6 that identifies the
		specific request. \n
			:param msi: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(msi)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:MSI {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:MSI \n
		The command sets the MSI subfield. MRQ = 0 When the MRQ subfield is set to 0, the MSI subfield is reserved. MRQ = 1 When
		the MRQ subfield is set to 1, the MSI subfield contains a sequence number in the range 0 to 6 that identifies the
		specific request. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: msi: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:MSI?')
		return Conversions.str_to_str_list(response)
