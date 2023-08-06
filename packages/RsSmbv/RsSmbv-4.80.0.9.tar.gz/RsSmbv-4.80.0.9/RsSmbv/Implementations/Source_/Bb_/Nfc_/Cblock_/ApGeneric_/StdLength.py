from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StdLength:
	"""StdLength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stdLength", core, parent)

	def get(self, std_frame_data_len: int, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:APGeneric:STDLength \n
		Shows the total length of a standard frame in bytes. \n
			:param std_frame_data_len: integer Range: 1 to 10
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: std_frame_data_len: integer Range: 1 to 10"""
		param = Conversions.decimal_value_to_str(std_frame_data_len)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:APGeneric:STDLength? {param}')
		return Conversions.str_to_int(response)
