from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TrptSubset:
	"""TrptSubset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trptSubset", core, parent)

	def set(self, trpt_subset: List[str], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RDATa:TRPTsubset \n
		The TRTP subset is a time resources pattern that indicates the set of available subframes to be used for sidelink
		communication. \n
			:param trpt_subset: 5 bits
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.list_to_csv_str(trpt_subset)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:RDATa:TRPTsubset {param}')

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RDATa:TRPTsubset \n
		The TRTP subset is a time resources pattern that indicates the set of available subframes to be used for sidelink
		communication. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: trpt_subset: 5 bits"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:RDATa:TRPTsubset?')
		return Conversions.str_to_str_list(response)
