from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Value:
	"""Value commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("value", core, parent)

	def set(self, offset: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:OFFSet<CH>:VALue \n
		Specifies Offset0 to Offset5 of the offset setting table. Command sets the values in ms. Query returns values in s. \n
			:param offset: float Range: 0 s to depending on Max. Interval , Unit: ms
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Offset')"""
		param = Conversions.decimal_value_to_str(offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:OFFSet{channel_cmd_val}:VALue {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:OFFSet<CH>:VALue \n
		Specifies Offset0 to Offset5 of the offset setting table. Command sets the values in ms. Query returns values in s. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Offset')
			:return: offset: float Range: 0 s to depending on Max. Interval , Unit: ms"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:OFFSet{channel_cmd_val}:VALue?')
		return Conversions.str_to_float(response)
