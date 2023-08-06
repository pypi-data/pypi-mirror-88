from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SfOffset:
	"""SfOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sfOffset", core, parent)

	def set(self, sys_frm_num_off: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SYINfo:SFOFfset \n
		Sets an offset value for the system frame number. The first generated frame starts with the given system frame number
		offset. \n
			:param sys_frm_num_off: integer Range: 0 to 1023
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(sys_frm_num_off)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SYINfo:SFOFfset {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SYINfo:SFOFfset \n
		Sets an offset value for the system frame number. The first generated frame starts with the given system frame number
		offset. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: sys_frm_num_off: integer Range: 0 to 1023"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SYINfo:SFOFfset?')
		return Conversions.str_to_int(response)
