from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, bbin_iq_hs_chan_sta: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:BB:STATe \n
		Activates the channel. \n
			:param bbin_iq_hs_chan_sta: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(bbin_iq_hs_chan_sta)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:BB:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:BB:STATe \n
		Activates the channel. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: bbin_iq_hs_chan_sta: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:BB:STATe?')
		return Conversions.str_to_bool(response)
