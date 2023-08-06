from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AcConstraint:
	"""AcConstraint commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acConstraint", core, parent)

	def set(self, ac_constraint: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:ACConstraint \n
		Sets the value for the AC signal field. 0 = The response may contain data from any TID (Traffic Identifier) . 1 = The
		response may contain data only from the same AC as the last Data received from the initiator. \n
			:param ac_constraint: integer Range: #H0,1 to #H1,1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(ac_constraint)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:ACConstraint {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:ACConstraint \n
		Sets the value for the AC signal field. 0 = The response may contain data from any TID (Traffic Identifier) . 1 = The
		response may contain data only from the same AC as the last Data received from the initiator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ac_constraint: integer Range: #H0,1 to #H1,1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:ACConstraint?')
		return Conversions.str_to_str_list(response)
