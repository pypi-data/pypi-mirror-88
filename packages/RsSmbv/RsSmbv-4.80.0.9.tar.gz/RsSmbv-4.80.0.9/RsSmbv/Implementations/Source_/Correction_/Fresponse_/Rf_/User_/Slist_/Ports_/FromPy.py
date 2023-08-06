from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FromPy:
	"""FromPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fromPy", core, parent)

	def set(self, freq_resp_sli_st_fr: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:SLISt<CH>:PORTs:FROM \n
		Sets the port number from that the signal is coming and the port to that it is going. Available ports depend on the file
		content and file extenssion, see 'S-Parameters (Touchstone) Files'. \n
			:param freq_resp_sli_st_fr: integer Range: 1 to 8 (dynamic)
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(freq_resp_sli_st_fr)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:SLISt{channel_cmd_val}:PORTs:FROM {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:SLISt<CH>:PORTs:FROM \n
		Sets the port number from that the signal is coming and the port to that it is going. Available ports depend on the file
		content and file extenssion, see 'S-Parameters (Touchstone) Files'. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: freq_resp_sli_st_fr: integer Range: 1 to 8 (dynamic)"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:SLISt{channel_cmd_val}:PORTs:FROM?')
		return Conversions.str_to_int(response)
