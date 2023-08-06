from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfactor:
	"""Cfactor commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfactor", core, parent)

	def set(self, bbin_iq_hs_ch_cr_fac: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:POWer:CFACtor \n
		Sets the crest factor of the individual channels. \n
			:param bbin_iq_hs_ch_cr_fac: float Range: 0 to 30
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(bbin_iq_hs_ch_cr_fac)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:POWer:CFACtor {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:POWer:CFACtor \n
		Sets the crest factor of the individual channels. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: bbin_iq_hs_ch_cr_fac: float Range: 0 to 30"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:POWer:CFACtor?')
		return Conversions.str_to_float(response)
