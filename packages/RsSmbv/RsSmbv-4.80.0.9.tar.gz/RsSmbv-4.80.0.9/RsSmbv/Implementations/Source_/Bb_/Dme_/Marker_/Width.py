from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Width:
	"""Width commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("width", core, parent)

	def set(self, width: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:[BB]:DME:MARKer<CH>:WIDTh \n
		Sets the width of the corresponding marker in chips (0.05us) . \n
			:param width: integer Range: 1 to 127
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')"""
		param = Conversions.decimal_value_to_str(width)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:MARKer{channel_cmd_val}:WIDTh {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:[BB]:DME:MARKer<CH>:WIDTh \n
		Sets the width of the corresponding marker in chips (0.05us) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')
			:return: width: integer Range: 1 to 127"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DME:MARKer{channel_cmd_val}:WIDTh?')
		return Conversions.str_to_int(response)
