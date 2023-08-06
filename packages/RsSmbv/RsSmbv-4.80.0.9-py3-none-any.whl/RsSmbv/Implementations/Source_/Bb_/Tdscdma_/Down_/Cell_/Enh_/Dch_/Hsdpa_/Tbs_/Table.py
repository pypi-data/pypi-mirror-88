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

	def set(self, table: enums.TdscdmaEnhHsTbsTableDn, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:TBS:TABLe \n
		Sets the transport block size table, according to the specification 3GPP TS 25.321. \n
			:param table: C1TO3| C4TO6| C10TO12| C7TO9| C13TO15| C16TO18| C19TO21| C22TO24
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(table, enums.TdscdmaEnhHsTbsTableDn)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSDPA:TBS:TABLe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TdscdmaEnhHsTbsTableDn:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:TBS:TABLe \n
		Sets the transport block size table, according to the specification 3GPP TS 25.321. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: table: C1TO3| C4TO6| C10TO12| C7TO9| C13TO15| C16TO18| C19TO21| C22TO24"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSDPA:TBS:TABLe?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaEnhHsTbsTableDn)
