from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class N3Pdsch:
	"""N3Pdsch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("n3Pdsch", core, parent)

	def set(self, n_3_pdsch: enums.EutraSlN3Pdsch, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RDISc:N3PDsch \n
		Sets the PDSCH resource index. \n
			:param n_3_pdsch: 1| 5
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(n_3_pdsch, enums.EutraSlN3Pdsch)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:RDISc:N3PDsch {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraSlN3Pdsch:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RDISc:N3PDsch \n
		Sets the PDSCH resource index. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: n_3_pdsch: 1| 5"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:RDISc:N3PDsch?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSlN3Pdsch)
