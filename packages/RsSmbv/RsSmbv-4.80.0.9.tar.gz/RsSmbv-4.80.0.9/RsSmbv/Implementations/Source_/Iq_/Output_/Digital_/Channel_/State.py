from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, dig_iq_hs_out_ch_sta: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:CHANnel<ST>:STATe \n
		Activates the channel. \n
			:param dig_iq_hs_out_ch_sta: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(dig_iq_hs_out_ch_sta)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:CHANnel{stream_cmd_val}:STATe {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce]:IQ:OUTPut:DIGital:CHANnel<ST>:STATe \n
		Activates the channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: dig_iq_hs_out_ch_sta: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:CHANnel{stream_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
