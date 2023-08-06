from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bits:
	"""Bits commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bits", core, parent)

	def set(self, bits: int, carrierComponent=repcap.CarrierComponent.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:[CELL<CCIDX>]:[SUBF<ST>]:ALLoc<CH>:PUSCh:HARQ:BITS \n
		Sets the number of ACK/NACK bits. Set this parameter to 0 to deactivate the ACK/NACK transmission for the corresponding
		subframe. \n
			:param bits: integer Range: 0 to dynamic
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(bits)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:CELL{carrierComponent_cmd_val}:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUSCh:HARQ:BITS {param}')

	def get(self, carrierComponent=repcap.CarrierComponent.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:[CELL<CCIDX>]:[SUBF<ST>]:ALLoc<CH>:PUSCh:HARQ:BITS \n
		Sets the number of ACK/NACK bits. Set this parameter to 0 to deactivate the ACK/NACK transmission for the corresponding
		subframe. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: bits: integer Range: 0 to dynamic"""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:CELL{carrierComponent_cmd_val}:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUSCh:HARQ:BITS?')
		return Conversions.str_to_int(response)
