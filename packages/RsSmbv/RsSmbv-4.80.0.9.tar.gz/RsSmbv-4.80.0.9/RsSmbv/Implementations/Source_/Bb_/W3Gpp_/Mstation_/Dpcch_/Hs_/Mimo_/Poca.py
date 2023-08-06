from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Poca:
	"""Poca commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poca", core, parent)

	def set(self, poca: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:MIMO:POCA \n
		(up to Release 7) Sets the power offset Poff_CQI Type A of the PCI/CQI slots in case a CQI Type A report is sent relative
		to the CQI Power PCQI (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Power.set) . The power PCQI Type A used during the
		PCI/CQI slots is calculated as: PCQI Type A = PCQI + Poff_CQI Type A Since the CQI Type B reports are used in a single
		stream transmission, the power PCQI Type B= PCQI. \n
			:param poca: float Range: -10 to 10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(poca)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:MIMO:POCA {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:MIMO:POCA \n
		(up to Release 7) Sets the power offset Poff_CQI Type A of the PCI/CQI slots in case a CQI Type A report is sent relative
		to the CQI Power PCQI (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Power.set) . The power PCQI Type A used during the
		PCI/CQI slots is calculated as: PCQI Type A = PCQI + Poff_CQI Type A Since the CQI Type B reports are used in a single
		stream transmission, the power PCQI Type B= PCQI. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: poca: float Range: -10 to 10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:MIMO:POCA?')
		return Conversions.str_to_float(response)
