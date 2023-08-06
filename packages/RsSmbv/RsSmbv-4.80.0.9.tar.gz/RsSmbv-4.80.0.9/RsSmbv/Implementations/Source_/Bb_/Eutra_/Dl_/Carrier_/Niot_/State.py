from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:STATe \n
		Enables the selected NB-IoT carrier. To enable the NB-IoT configuration, enable the anchor carrier
		(SOURce1:BB:EUTRa:DL:CARRier0NIOT:STATe1) \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:STATe \n
		Enables the selected NB-IoT carrier. To enable the NB-IoT configuration, enable the anchor carrier
		(SOURce1:BB:EUTRa:DL:CARRier0NIOT:STATe1) \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:STATe?')
		return Conversions.str_to_bool(response)
