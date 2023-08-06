from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def set(self, dig_iq_hs_srat_chan: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:CHANnel<ST>:SRATe \n
		Sets the sample rate per channel. \n
			:param dig_iq_hs_srat_chan: float Range: 400 to 600E6
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(dig_iq_hs_srat_chan)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:CHANnel{stream_cmd_val}:SRATe {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce]:IQ:OUTPut:DIGital:CHANnel<ST>:SRATe \n
		Sets the sample rate per channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: dig_iq_hs_srat_chan: float Range: 400 to 600E6"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:CHANnel{stream_cmd_val}:SRATe?')
		return Conversions.str_to_float(response)
