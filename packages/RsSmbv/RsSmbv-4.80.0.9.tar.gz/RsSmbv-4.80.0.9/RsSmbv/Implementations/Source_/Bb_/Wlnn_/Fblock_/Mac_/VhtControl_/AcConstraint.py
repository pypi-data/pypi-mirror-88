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

	def set(self, vht_ac_constraint: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:ACConstraint \n
		The command sets the value for the AC signal field. It indicates the access point of the responder (1 bit) . \n
			:param vht_ac_constraint: integer 0 The response may contain data from any TID (Traffic Identifier) 1 The response may contain data only from the same AC as the last data received from the initiator.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(vht_ac_constraint)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:ACConstraint {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:ACConstraint \n
		The command sets the value for the AC signal field. It indicates the access point of the responder (1 bit) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: vht_ac_constraint: integer 0 The response may contain data from any TID (Traffic Identifier) 1 The response may contain data only from the same AC as the last data received from the initiator."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:ACConstraint?')
		return Conversions.str_to_str_list(response)
