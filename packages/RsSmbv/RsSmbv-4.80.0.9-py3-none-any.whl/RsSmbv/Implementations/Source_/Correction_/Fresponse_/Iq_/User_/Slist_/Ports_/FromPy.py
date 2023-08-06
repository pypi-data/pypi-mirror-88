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

	def set(self, freq_corr_iq_po_fro: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:SLISt<CH>:PORTs:FROM \n
		No command help available \n
			:param freq_corr_iq_po_fro: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(freq_corr_iq_po_fro)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:SLISt{channel_cmd_val}:PORTs:FROM {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:SLISt<CH>:PORTs:FROM \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: freq_corr_iq_po_fro: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:SLISt{channel_cmd_val}:PORTs:FROM?')
		return Conversions.str_to_int(response)
