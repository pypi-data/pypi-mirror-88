from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PoaNack:
	"""PoaNack commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poaNack", core, parent)

	def set(self, poa_nack: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:MIMO:POANack \n
		(up to Release 7) Sets the power offset Poff_ACK/NACK of an ACK/NACK response to two scheduled transport blocks relative
		to the CQI Power PCQI (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Power.set) . The power PACK/NACK used during the
		HARQ-ACK slots is calculated as: PACK/NACK = PCQI + Poff_ACK/NACK \n
			:param poa_nack: float Range: -10 to 10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(poa_nack)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:MIMO:POANack {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:MIMO:POANack \n
		(up to Release 7) Sets the power offset Poff_ACK/NACK of an ACK/NACK response to two scheduled transport blocks relative
		to the CQI Power PCQI (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Power.set) . The power PACK/NACK used during the
		HARQ-ACK slots is calculated as: PACK/NACK = PCQI + Poff_ACK/NACK \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: poa_nack: float Range: -10 to 10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:MIMO:POANack?')
		return Conversions.str_to_float(response)
