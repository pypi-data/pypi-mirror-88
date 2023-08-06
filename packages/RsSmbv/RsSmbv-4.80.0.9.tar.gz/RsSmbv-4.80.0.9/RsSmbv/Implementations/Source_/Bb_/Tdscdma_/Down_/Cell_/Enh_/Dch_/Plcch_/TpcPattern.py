from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpcPattern:
	"""TpcPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tpcPattern", core, parent)

	# noinspection PyTypeChecker
	class TpcPatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Tpc_Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 21"""
		__meta_args_list = [
			ArgStruct('Tpc_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tpc_Pattern: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: TpcPatternStruct, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:PLCCh:TPCPattern \n
		Sets the TPC pattern and the pattern length. \n
			:param structure: for set value, see the help for TpcPatternStruct structure arguments.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:PLCCh:TPCPattern', structure)

	def get(self, stream=repcap.Stream.Default) -> TpcPatternStruct:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:PLCCh:TPCPattern \n
		Sets the TPC pattern and the pattern length. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: structure: for return value, see the help for TpcPatternStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:PLCCh:TPCPattern?', self.__class__.TpcPatternStruct())
