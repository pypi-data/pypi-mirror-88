from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Values:
	"""Values commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("values", core, parent)

	def set(self, values: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:CQI<CH>:[VALues] \n
		Sets the values of the CQI sequence. The length of the CQI sequence is defined with command method RsSmbv.Source.Bb.W3Gpp.
		Mstation.Dpcch.Hs.Cqi.Plength.set. The pattern is generated cyclically. \n
			:param values: integer Value -1 means that no CQI is sent (DTX - Discontinuous Transmission) . Range: -1 to 30
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cqi')"""
		param = Conversions.decimal_value_to_str(values)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:CQI{channel_cmd_val}:VALues {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:CQI<CH>:[VALues] \n
		Sets the values of the CQI sequence. The length of the CQI sequence is defined with command method RsSmbv.Source.Bb.W3Gpp.
		Mstation.Dpcch.Hs.Cqi.Plength.set. The pattern is generated cyclically. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cqi')
			:return: values: integer Value -1 means that no CQI is sent (DTX - Discontinuous Transmission) . Range: -1 to 30"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:CQI{channel_cmd_val}:VALues?')
		return Conversions.str_to_int(response)
