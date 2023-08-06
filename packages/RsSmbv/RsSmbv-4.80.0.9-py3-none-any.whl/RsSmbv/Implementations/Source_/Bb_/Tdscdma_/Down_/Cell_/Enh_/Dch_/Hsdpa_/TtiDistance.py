from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TtiDistance:
	"""TtiDistance commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ttiDistance", core, parent)

	def set(self, tti_distance: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:TTIDistance \n
		Sets the inter-TTI distance. The inter-TTI is the distance between two packets in HSDPA packet mode and determines
		whether data is sent each TTI or there is a DTX transmission in some of the TTIs. An inter-TTI distance of 1 means
		continuous generation. \n
			:param tti_distance: integer Range: 1 to 8
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(tti_distance)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSDPA:TTIDistance {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:TTIDistance \n
		Sets the inter-TTI distance. The inter-TTI is the distance between two packets in HSDPA packet mode and determines
		whether data is sent each TTI or there is a DTX transmission in some of the TTIs. An inter-TTI distance of 1 means
		continuous generation. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: tti_distance: integer Range: 1 to 8"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSDPA:TTIDistance?')
		return Conversions.str_to_int(response)
