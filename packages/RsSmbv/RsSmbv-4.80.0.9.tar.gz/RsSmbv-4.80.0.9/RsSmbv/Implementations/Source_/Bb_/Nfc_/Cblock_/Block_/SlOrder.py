from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlOrder:
	"""SlOrder commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slOrder", core, parent)

	def set(self, scl_order: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:SLORder \n
		Sets the service code list order. \n
			:param scl_order: integer Range: 0 to dynamic
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')"""
		param = Conversions.decimal_value_to_str(scl_order)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BLOCk{stream_cmd_val}:SLORder {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:SLORder \n
		Sets the service code list order. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
			:return: scl_order: integer Range: 0 to dynamic"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BLOCk{stream_cmd_val}:SLORder?')
		return Conversions.str_to_int(response)
