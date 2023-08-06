from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcsr:
	"""Mcsr commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcsr", core, parent)

	def set(self, mcsr: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:DCIConf:MCSR \n
		Sets the DCI formats 1/1B/1D/2/2A/2B/2C/2D field modulation and coding scheme. \n
			:param mcsr: integer Range: 0 to depends on the installed options Option: R&S SMBVB-K55 max = 31 Option: R&S SMBVB-K119 max = 63 Values 32 to 63 available if method RsSmbv.Source.Bb.Eutra.Dl.User.Cell.Mcs.set T4.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')"""
		param = Conversions.decimal_value_to_str(mcsr)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:DCIConf:MCSR {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:DCIConf:MCSR \n
		Sets the DCI formats 1/1B/1D/2/2A/2B/2C/2D field modulation and coding scheme. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')
			:return: mcsr: integer Range: 0 to depends on the installed options Option: R&S SMBVB-K55 max = 31 Option: R&S SMBVB-K119 max = 63 Values 32 to 63 available if method RsSmbv.Source.Bb.Eutra.Dl.User.Cell.Mcs.set T4."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:DCIConf:MCSR?')
		return Conversions.str_to_int(response)
