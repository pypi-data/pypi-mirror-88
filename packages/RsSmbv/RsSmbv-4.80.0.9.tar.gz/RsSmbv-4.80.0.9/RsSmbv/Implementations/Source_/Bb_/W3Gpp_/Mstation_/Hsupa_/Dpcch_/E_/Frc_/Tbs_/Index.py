from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Index:
	"""Index commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("index", core, parent)

	def set(self, index: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:TBS:INDex \n
		Selects the Transport Block Size Index (E-TFCI) for the corresponding table, as described in in 3GPP TS 25.321, Annex B.
		The value range of this parameter depends on the selected Transport Block Size Table (BB:W3GPp:DPCCh:E:FRC:TBS:TABLe) . \n
			:param index: integer Range: 0 to max
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(index)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:FRC:TBS:INDex {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:TBS:INDex \n
		Selects the Transport Block Size Index (E-TFCI) for the corresponding table, as described in in 3GPP TS 25.321, Annex B.
		The value range of this parameter depends on the selected Transport Block Size Table (BB:W3GPp:DPCCh:E:FRC:TBS:TABLe) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: index: integer Range: 0 to max"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:FRC:TBS:INDex?')
		return Conversions.str_to_int(response)
