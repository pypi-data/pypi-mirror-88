from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channel", core, parent)

	def set(self, channel_param: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:DOWN:MC:CARRier<CH>:CHANnel \n
		Sets carrier’s CDMA channel number. The available Channel values depend on the selected Band Class. In some cases, not
		all channel numbers can be used. In case a non-existing channel is input, the next available channel is used. \n
			:param channel_param: integer Range: 0 to 3000
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.decimal_value_to_str(channel_param)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:DOWN:MC:CARRier{channel_cmd_val}:CHANnel {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:DOWN:MC:CARRier<CH>:CHANnel \n
		Sets carrier’s CDMA channel number. The available Channel values depend on the selected Band Class. In some cases, not
		all channel numbers can be used. In case a non-existing channel is input, the next available channel is used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: channel_param: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:DOWN:MC:CARRier{channel_cmd_val}:CHANnel?')
		return Conversions.str_to_int(response)
