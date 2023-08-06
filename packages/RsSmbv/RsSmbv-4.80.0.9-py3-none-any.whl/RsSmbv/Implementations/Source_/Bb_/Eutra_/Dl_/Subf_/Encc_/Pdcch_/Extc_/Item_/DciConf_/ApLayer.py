from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApLayer:
	"""ApLayer commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apLayer", core, parent)

	def set(self, ap_layer_id: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:DCIConf:APLayer \n
		Sets the DCI Format 2C field antenna port(s) , layer, scrambling Id. Option: R&S SMBVB-K119: Value range <ApLayerId>
			Table Header: method RsSmbv.Source.Bb.Eutra.Dl.User.Cell.Dmrs.State.set / method RsSmbv.Source.Bb.Eutra.Dl.User.Cell.Seol.State.set / 1 codeword / 2 codewords \n
			- 0 / 0 / 0 to 6 / 0 to 7
			- 1 / 0 / 0 to 11 / 0 to 14
			- 1 / 1 / 0 to 1 / 0 to 1 \n
			:param ap_layer_id: integer Range: 0 to 7
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')"""
		param = Conversions.decimal_value_to_str(ap_layer_id)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:DCIConf:APLayer {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:DCIConf:APLayer \n
		Sets the DCI Format 2C field antenna port(s) , layer, scrambling Id. Option: R&S SMBVB-K119: Value range <ApLayerId>
			Table Header: method RsSmbv.Source.Bb.Eutra.Dl.User.Cell.Dmrs.State.set / method RsSmbv.Source.Bb.Eutra.Dl.User.Cell.Seol.State.set / 1 codeword / 2 codewords \n
			- 0 / 0 / 0 to 6 / 0 to 7
			- 1 / 0 / 0 to 11 / 0 to 14
			- 1 / 1 / 0 to 1 / 0 to 1 \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')
			:return: ap_layer_id: integer Range: 0 to 7"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:DCIConf:APLayer?')
		return Conversions.str_to_int(response)
