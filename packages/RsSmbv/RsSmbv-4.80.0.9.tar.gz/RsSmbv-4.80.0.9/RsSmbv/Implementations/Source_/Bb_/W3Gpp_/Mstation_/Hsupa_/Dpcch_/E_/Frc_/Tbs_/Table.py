from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Table:
	"""Table commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("table", core, parent)

	def set(self, table: enums.HsUpaFrcTable, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:TBS:TABLe \n
		Selects the Transport Block Size Table from 3GPP TS 25.321, Annex B according to that the transport block size is
		configured. The transport block size is determined also by the Transport Block Size Index
		(BB:W3GPp:DPCCh:E:FRC:TBS:INDex) . The allowed values for this command depend on the selected E-DCH TTI
		(BB:W3GPp:DPCCh:E:FRC:TTIEdch) and modulation scheme (BB:W3GPp:DPCCh:E:FRC:MODulation) .
			Table Header: E-DCH TTI / Modulation / Transport Block Size Table / SCPI Paramater / Transport Block Size Index (E-TFCI) \n
			- 2ms / BPSK / Table 0 / TAB0TTI2 / 0 .. 127
			- Table 1 / TAB1TTI2 / 0 .. 125
			- 4PAM / Table 2 / TAB2TTI2 / 0 .. 127
			- Table 3 / TAB3TTI2 / 0 .. 124
			- 10ms / Table 0 / TAB0TTI10 / 0 .. 127
			- Table 1 / TAB1TTI10 / 0 .. 120 \n
			:param table: TAB0TTI2| TAB1TTI2| TAB2TTI2| TAB3TTI2| TAB0TTI10| TAB1TTI10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(table, enums.HsUpaFrcTable)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:FRC:TBS:TABLe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.HsUpaFrcTable:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:TBS:TABLe \n
		Selects the Transport Block Size Table from 3GPP TS 25.321, Annex B according to that the transport block size is
		configured. The transport block size is determined also by the Transport Block Size Index
		(BB:W3GPp:DPCCh:E:FRC:TBS:INDex) . The allowed values for this command depend on the selected E-DCH TTI
		(BB:W3GPp:DPCCh:E:FRC:TTIEdch) and modulation scheme (BB:W3GPp:DPCCh:E:FRC:MODulation) .
			Table Header: E-DCH TTI / Modulation / Transport Block Size Table / SCPI Paramater / Transport Block Size Index (E-TFCI) \n
			- 2ms / BPSK / Table 0 / TAB0TTI2 / 0 .. 127
			- Table 1 / TAB1TTI2 / 0 .. 125
			- 4PAM / Table 2 / TAB2TTI2 / 0 .. 127
			- Table 3 / TAB3TTI2 / 0 .. 124
			- 10ms / Table 0 / TAB0TTI10 / 0 .. 127
			- Table 1 / TAB1TTI10 / 0 .. 120 \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: table: TAB0TTI2| TAB1TTI2| TAB2TTI2| TAB3TTI2| TAB0TTI10| TAB1TTI10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:FRC:TBS:TABLe?')
		return Conversions.str_to_scalar_enum(response, enums.HsUpaFrcTable)
