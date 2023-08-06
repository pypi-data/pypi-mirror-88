from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TtiDistance:
	"""TtiDistance commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ttiDistance", core, parent)

	def set(self, tti_distance: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:TTIDistance \n
		Selects the distance between two packets in HSDPA packet mode. \n
			:param tti_distance: integer Range: 1 to 16
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(tti_distance)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:TTIDistance {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:TTIDistance \n
		Selects the distance between two packets in HSDPA packet mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: tti_distance: integer Range: 1 to 16"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:TTIDistance?')
		return Conversions.str_to_int(response)
