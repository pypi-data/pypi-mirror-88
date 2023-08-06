from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Name:
	"""Name commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("name", core, parent)

	def set(self, dig_iq_hs_ch_name: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:CHANnel<ST>:NAME \n
		Sets the channel name. \n
			:param dig_iq_hs_ch_name: string
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.value_to_quoted_str(dig_iq_hs_ch_name)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:CHANnel{stream_cmd_val}:NAME {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce]:IQ:OUTPut:DIGital:CHANnel<ST>:NAME \n
		Sets the channel name. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: dig_iq_hs_ch_name: string"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:CHANnel{stream_cmd_val}:NAME?')
		return trim_str_response(response)
