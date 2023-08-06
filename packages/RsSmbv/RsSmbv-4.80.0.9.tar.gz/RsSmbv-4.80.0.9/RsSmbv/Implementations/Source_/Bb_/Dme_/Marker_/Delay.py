from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def set(self, delay: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:[BB]:DME:MARKer<CH>:DELay \n
		Sets the delay between the marker signal at the marker outputs relative to the signal generation start. \n
			:param delay: integer Range: 0 to 127
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')"""
		param = Conversions.decimal_value_to_str(delay)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:MARKer{channel_cmd_val}:DELay {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:[BB]:DME:MARKer<CH>:DELay \n
		Sets the delay between the marker signal at the marker outputs relative to the signal generation start. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')
			:return: delay: integer Range: 0 to 127"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DME:MARKer{channel_cmd_val}:DELay?')
		return Conversions.str_to_int(response)
