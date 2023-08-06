from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("select", core, parent)

	def set(self, freq_corr_iq_sl_sel: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:SLISt<CH>:SELect \n
		No command help available \n
			:param freq_corr_iq_sl_sel: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.value_to_quoted_str(freq_corr_iq_sl_sel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:SLISt{channel_cmd_val}:SELect {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:SLISt<CH>:SELect \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: freq_corr_iq_sl_sel: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:SLISt{channel_cmd_val}:SELect?')
		return trim_str_response(response)
