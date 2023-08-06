from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FbIndex:
	"""FbIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fbIndex", core, parent)

	def set(self, fb_index: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut<CH>:FBINdex \n
		Sets the frame block index. For this/these frame block(s) , a marker signal is generated. The maximum value depends on
		the number of the currently active frame blocks (max = 100) . \n
			:param fb_index: integer Range: 0 to 100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(fb_index)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut{channel_cmd_val}:FBINdex {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut<CH>:FBINdex \n
		Sets the frame block index. For this/these frame block(s) , a marker signal is generated. The maximum value depends on
		the number of the currently active frame blocks (max = 100) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: fb_index: integer Range: 0 to 100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut{channel_cmd_val}:FBINdex?')
		return Conversions.str_to_int(response)
