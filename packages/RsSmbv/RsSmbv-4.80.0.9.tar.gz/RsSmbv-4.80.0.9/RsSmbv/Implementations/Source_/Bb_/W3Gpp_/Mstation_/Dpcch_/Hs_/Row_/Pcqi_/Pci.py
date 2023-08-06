from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pci:
	"""Pci commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pci", core, parent)

	def set(self, pci: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:PCQI<DI>:PCI \n
		No command help available \n
			:param pci: integer Range: 0 to 3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Pcqi')"""
		param = Conversions.decimal_value_to_str(pci)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:PCQI{twoStreams_cmd_val}:PCI {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:PCQI<DI>:PCI \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Pcqi')
			:return: pci: integer Range: 0 to 3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:PCQI{twoStreams_cmd_val}:PCI?')
		return Conversions.str_to_int(response)
