from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RdgMore:
	"""RdgMore commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rdgMore", core, parent)

	def set(self, rdg_more: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:RDGMore \n
		Sets the value for the RDG/More PPDU. Transmitted by Initiator 0 = No reverse grant. 1 = A reverse grant is present, as
		defined by the Duration/ID field. Transmitted by Responder 0 = The PPDU carrying the MPDU is the last transmission by the
		responder. 1 = The PPDU carrying the frame is followed by another PPDU. \n
			:param rdg_more: integer Range: #H0,1 to #H1,1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(rdg_more)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:RDGMore {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:RDGMore \n
		Sets the value for the RDG/More PPDU. Transmitted by Initiator 0 = No reverse grant. 1 = A reverse grant is present, as
		defined by the Duration/ID field. Transmitted by Responder 0 = The PPDU carrying the MPDU is the last transmission by the
		responder. 1 = The PPDU carrying the frame is followed by another PPDU. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: rdg_more: integer Range: #H0,1 to #H1,1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:RDGMore?')
		return Conversions.str_to_str_list(response)
