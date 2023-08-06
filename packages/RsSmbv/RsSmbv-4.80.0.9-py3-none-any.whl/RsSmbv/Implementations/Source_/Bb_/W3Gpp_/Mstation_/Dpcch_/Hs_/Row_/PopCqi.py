from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PopCqi:
	"""PopCqi commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("popCqi", core, parent)

	def set(self, po_pcqi: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:POPCqi \n
		(Release 8 and Later) Sets the power offset Poff_PCI/CQI of all PCI/CQI slots during the corresponding specified PCI/CQI
		From/To range relative to the method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Power.set. \n
			:param po_pcqi: float Range: -10 to 10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(po_pcqi)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:POPCqi {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:POPCqi \n
		(Release 8 and Later) Sets the power offset Poff_PCI/CQI of all PCI/CQI slots during the corresponding specified PCI/CQI
		From/To range relative to the method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Power.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:return: po_pcqi: float Range: -10 to 10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:POPCqi?')
		return Conversions.str_to_float(response)
