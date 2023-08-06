from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LaControl:
	"""LaControl commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("laControl", core, parent)

	def set(self, la_control: List[str], channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:LAControl \n
		Sets the value for the link adaption control. B0 (1bit) MA - MA payload When the MA field is set to 1, the payload of the
		QoS Null Data MPDU is interpreted as a payload of the management action frame. B1 (1bit) TRQ - Sounding Request 1 =
		Request to the responder to transmit a sounding PPDU. B2 (1bit) MRQ - MCS Request 1 = Request for feedback of MCS. B3-B5
		(3bit) MRS - MRQ Sequence Identifier Set by sender to any value in the range '000'-'110' to identify MRQ. = Invalid if
		MRQ = 0 B6-B8 (3bit) MFS - MFB Sequence Identifier Set to the received value of MRS. Set to '111' for unsolicited MFB.
		B9-B15 (7bit) MFB - MCS Feedback Link adaptation feedback containing the recommended MCS. When a responder is unable to
		provide MCS feedback or the feedback is not available, the MFB is set to 'all-ones' (default value) and also MFS is set
		to '1'. \n
			:param la_control: integer Range: #H0000,16 to #HFFFF, 16
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(la_control)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:LAControl {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:LAControl \n
		Sets the value for the link adaption control. B0 (1bit) MA - MA payload When the MA field is set to 1, the payload of the
		QoS Null Data MPDU is interpreted as a payload of the management action frame. B1 (1bit) TRQ - Sounding Request 1 =
		Request to the responder to transmit a sounding PPDU. B2 (1bit) MRQ - MCS Request 1 = Request for feedback of MCS. B3-B5
		(3bit) MRS - MRQ Sequence Identifier Set by sender to any value in the range '000'-'110' to identify MRQ. = Invalid if
		MRQ = 0 B6-B8 (3bit) MFS - MFB Sequence Identifier Set to the received value of MRS. Set to '111' for unsolicited MFB.
		B9-B15 (7bit) MFB - MCS Feedback Link adaptation feedback containing the recommended MCS. When a responder is unable to
		provide MCS feedback or the feedback is not available, the MFB is set to 'all-ones' (default value) and also MFS is set
		to '1'. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: la_control: integer Range: #H0000,16 to #HFFFF, 16"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:HTControl:LAControl?')
		return Conversions.str_to_str_list(response)
