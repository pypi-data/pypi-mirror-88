from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nzpnum:
	"""Nzpnum commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nzpnum", core, parent)

	def set(self, num_non_zero_pwr_co: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:NZPNum \n
		Enables up to 96 NonZeroTxPower CSI-RS within the DRS period. \n
			:param num_non_zero_pwr_co: integer Range: 0 to 96
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(num_non_zero_pwr_co)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:NZPNum {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:NZPNum \n
		Enables up to 96 NonZeroTxPower CSI-RS within the DRS period. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: num_non_zero_pwr_co: integer Range: 0 to 96"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:NZPNum?')
		return Conversions.str_to_int(response)
