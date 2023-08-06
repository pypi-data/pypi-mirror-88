from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxopDuration:
	"""TxopDuration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("txopDuration", core, parent)

	def set(self, tx_op_duraion: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:TXOPduration \n
		If transmission opportunity (TXOP) is set to 127, it indicates no duration information. If it is set to any other value,
		it indicates duration information for network allocation vector (NAV) parameter and that the TXOP is protected. \n
			:param tx_op_duraion: integer Range: 0 to 127
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.decimal_value_to_str(tx_op_duraion)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:TXOPduration {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:TXOPduration \n
		If transmission opportunity (TXOP) is set to 127, it indicates no duration information. If it is set to any other value,
		it indicates duration information for network allocation vector (NAV) parameter and that the TXOP is protected. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: tx_op_duraion: integer Range: 0 to 127"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:TXOPduration?')
		return Conversions.str_to_int(response)
