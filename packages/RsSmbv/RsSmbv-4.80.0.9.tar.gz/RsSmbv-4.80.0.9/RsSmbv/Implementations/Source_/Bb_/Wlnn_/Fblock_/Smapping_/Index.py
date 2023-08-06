from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Index:
	"""Index commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("index", core, parent)

	def set(self, index: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SMAPping:INDex \n
		Sets the index of the subcarrier. A matrix is mapped to each subcarrier. Except for k=0, the index can be set in the
		value range of -64 to 63 \n
			:param index: integer Range: depends on TxMode to depends on TxMode
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.decimal_value_to_str(index)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SMAPping:INDex {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SMAPping:INDex \n
		Sets the index of the subcarrier. A matrix is mapped to each subcarrier. Except for k=0, the index can be set in the
		value range of -64 to 63 \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: index: integer Range: depends on TxMode to depends on TxMode"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SMAPping:INDex?')
		return Conversions.str_to_int(response)
