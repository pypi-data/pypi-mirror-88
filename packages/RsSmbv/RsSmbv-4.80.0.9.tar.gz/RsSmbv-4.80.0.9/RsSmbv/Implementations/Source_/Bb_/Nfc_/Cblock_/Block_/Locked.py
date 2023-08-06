from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Locked:
	"""Locked commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("locked", core, parent)

	def set(self, lcontrol: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:LOCKed \n
		Enables/disables status information on lock for the corresponding block ('BLOCK-1' to 'BLOCK-C') . \n
			:param lcontrol: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')"""
		param = Conversions.bool_to_str(lcontrol)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BLOCk{stream_cmd_val}:LOCKed {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BLOCk<ST>:LOCKed \n
		Enables/disables status information on lock for the corresponding block ('BLOCK-1' to 'BLOCK-C') . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
			:return: lcontrol: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BLOCk{stream_cmd_val}:LOCKed?')
		return Conversions.str_to_bool(response)
