from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Len:
	"""Len commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("len", core, parent)

	def set(self, bl_length: enums.NfcLength, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:LEN \n
		Sets the block length. \n
			:param bl_length: LEN2| LEN3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')"""
		param = Conversions.enum_scalar_to_str(bl_length, enums.NfcLength)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BLOCk{stream_cmd_val}:LEN {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.NfcLength:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:LEN \n
		Sets the block length. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
			:return: bl_length: LEN2| LEN3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BLOCk{stream_cmd_val}:LEN?')
		return Conversions.str_to_scalar_enum(response, enums.NfcLength)
