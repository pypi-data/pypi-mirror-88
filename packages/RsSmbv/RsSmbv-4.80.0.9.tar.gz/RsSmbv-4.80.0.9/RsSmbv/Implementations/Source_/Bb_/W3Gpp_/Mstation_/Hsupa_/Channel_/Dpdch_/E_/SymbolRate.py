from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.WcdmaSymbRateEdPdchOverallSymbRate:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:CHANnel<CH>:DPDCh:E:SRATe \n
		The command queries the symbol rate and the state of the E-DPDCH channel. The symbol rate and the state of the channels
		are dependent on the overall symbol rate set and cannot be modified. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: srate: D15K| D30K| D60K| D120k| D240k| D480k| D960k| D1920k| D2X1920K| D2X960K2X1920K"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:CHANnel{channel_cmd_val}:DPDCh:E:SRATe?')
		return Conversions.str_to_scalar_enum(response, enums.WcdmaSymbRateEdPdchOverallSymbRate)
