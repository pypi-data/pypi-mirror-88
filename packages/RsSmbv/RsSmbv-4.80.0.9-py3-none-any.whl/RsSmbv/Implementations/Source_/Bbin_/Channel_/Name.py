from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Name:
	"""Name commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("name", core, parent)

	def set(self, bbin_iq_hs_chan_nam: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:NAME \n
		Queries the channel name. \n
			:param bbin_iq_hs_chan_nam: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.value_to_quoted_str(bbin_iq_hs_chan_nam)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:NAME {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:NAME \n
		Queries the channel name. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: bbin_iq_hs_chan_nam: string"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:NAME?')
		return trim_str_response(response)
