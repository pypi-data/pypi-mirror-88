from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Snumber:
	"""Snumber commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("snumber", core, parent)

	def set(self, snumber: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SERVice<ST>:SNUMber \n
		Determines the number of services. \n
			:param snumber: integer Range: 0 to 1023
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Service')"""
		param = Conversions.decimal_value_to_str(snumber)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SERVice{stream_cmd_val}:SNUMber {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:SERVice<ST>:SNUMber \n
		Determines the number of services. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Service')
			:return: snumber: integer Range: 0 to 1023"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:SERVice{stream_cmd_val}:SNUMber?')
		return Conversions.str_to_int(response)
