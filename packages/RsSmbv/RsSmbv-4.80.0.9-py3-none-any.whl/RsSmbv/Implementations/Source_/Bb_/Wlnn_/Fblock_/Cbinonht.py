from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cbinonht:
	"""Cbinonht commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cbinonht", core, parent)

	def set(self, cbi_nonht: enums.WlannFbChBwInNonHt, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:CBINonht \n
		(Available only for VHT Tx mode) The command is used to modify the first 7 bits of the scrambling sequence to indicate
		the duplicated bandwidth of the PPDU. \n
			:param cbi_nonht: B20| B40| B80| B160| OFF OFF Channel bandwidth in Non HT is not present. Unit: MHz
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(cbi_nonht, enums.WlannFbChBwInNonHt)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:CBINonht {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbChBwInNonHt:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:CBINonht \n
		(Available only for VHT Tx mode) The command is used to modify the first 7 bits of the scrambling sequence to indicate
		the duplicated bandwidth of the PPDU. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: cbi_nonht: B20| B40| B80| B160| OFF OFF Channel bandwidth in Non HT is not present. Unit: MHz"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:CBINonht?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbChBwInNonHt)
