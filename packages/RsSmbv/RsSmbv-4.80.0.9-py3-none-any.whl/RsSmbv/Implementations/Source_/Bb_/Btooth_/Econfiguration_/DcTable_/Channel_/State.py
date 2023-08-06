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
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:DCTable:CHANnel<CH>:STATe \n
		Indicates used and unused data channels. Note: The previously used syntax ..:SET<ch>:STATe has been replaced by ...
		:CHANnel<ch>:STATe. Compatibility to the previous commands is given. This parameter is relevant for data event and
		advertising frame configuration with the packet types LL_CHANNEL_MAP_IND, CONNECT_IND. Within the option R&S SMBVB-K117,
		the following packet types are also relevant for the setting: AUX_CONNECT_IND, AUX_EXT_IND, AUX_ADV_IND, AUX_CHAIN_IND,
		AUX_SYNC_IND, AUX_SCAN_RSP. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:DCTable:CHANnel{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:DCTable:CHANnel<CH>:STATe \n
		Indicates used and unused data channels. Note: The previously used syntax ..:SET<ch>:STATe has been replaced by ...
		:CHANnel<ch>:STATe. Compatibility to the previous commands is given. This parameter is relevant for data event and
		advertising frame configuration with the packet types LL_CHANNEL_MAP_IND, CONNECT_IND. Within the option R&S SMBVB-K117,
		the following packet types are also relevant for the setting: AUX_CONNECT_IND, AUX_EXT_IND, AUX_ADV_IND, AUX_CHAIN_IND,
		AUX_SYNC_IND, AUX_SCAN_RSP. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:DCTable:CHANnel{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
