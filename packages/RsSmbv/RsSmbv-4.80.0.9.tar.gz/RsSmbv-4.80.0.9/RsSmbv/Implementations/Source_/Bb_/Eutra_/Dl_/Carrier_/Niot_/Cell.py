from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)

	def set(self, cell_id: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:CELL \n
		Sets the narrowband physical cell identifier. \n
			:param cell_id: integer Range: 0 to 503
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.decimal_value_to_str(cell_id)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:CELL {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:CELL \n
		Sets the narrowband physical cell identifier. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: cell_id: integer Range: 0 to 503"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:CELL?')
		return Conversions.str_to_int(response)
