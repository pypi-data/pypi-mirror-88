from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def set(self, bbin_iq_hs_ch_sa_rat: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:SRATe \n
		Sets the sample rate per channel. \n
			:param bbin_iq_hs_ch_sa_rat: float Range: 400 to 250E6 ('System Config Mode = Advanced') /1250E6 ('System Config Mode = Standard')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(bbin_iq_hs_ch_sa_rat)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:SRATe {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:SRATe \n
		Sets the sample rate per channel. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: bbin_iq_hs_ch_sa_rat: float Range: 400 to 250E6 ('System Config Mode = Advanced') /1250E6 ('System Config Mode = Standard')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:SRATe?')
		return Conversions.str_to_float(response)
