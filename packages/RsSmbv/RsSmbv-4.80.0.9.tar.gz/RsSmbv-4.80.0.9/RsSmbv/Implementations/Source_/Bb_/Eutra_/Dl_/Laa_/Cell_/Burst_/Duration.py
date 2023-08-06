from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Duration:
	"""Duration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("duration", core, parent)

	def set(self, duration: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:DURation \n
		Sets the duration of the LAA burst. \n
			:param duration: integer Range: 1 to 10
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')"""
		param = Conversions.decimal_value_to_str(duration)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:DURation {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:DURation \n
		Sets the duration of the LAA burst. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')
			:return: duration: integer Range: 1 to 10"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:DURation?')
		return Conversions.str_to_int(response)
