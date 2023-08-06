from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SegSelection:
	"""SegSelection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("segSelection", core, parent)

	def set(self, segment_sel: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SEGSelection \n
		Selects a segment to be read. \n
			:param segment_sel: integer Range: 0 to 15
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.decimal_value_to_str(segment_sel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SEGSelection {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SEGSelection \n
		Selects a segment to be read. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: segment_sel: integer Range: 0 to 15"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SEGSelection?')
		return Conversions.str_to_int(response)
