from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BitHigh:
	"""BitHigh commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bitHigh", core, parent)

	# noinspection PyTypeChecker
	class BitHighStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 0 to 50"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: BitHighStruct, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:BITHigh \n
		Sets the subframe bitmap. [:SOURce<hw>]:BB:EUTRa:UL:UE<st>:SL:V2X:BITHigh is enabled, if method RsSmbv.Source.Bb.Eutra.Ul.
		Ue.Sl.V2X.BmpLength.set60|100. \n
			:param structure: for set value, see the help for BitHighStruct structure arguments.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:BITHigh', structure)

	def get(self, stream=repcap.Stream.Default) -> BitHighStruct:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:BITHigh \n
		Sets the subframe bitmap. [:SOURce<hw>]:BB:EUTRa:UL:UE<st>:SL:V2X:BITHigh is enabled, if method RsSmbv.Source.Bb.Eutra.Ul.
		Ue.Sl.V2X.BmpLength.set60|100. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: structure: for return value, see the help for BitHighStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:BITHigh?', self.__class__.BitHighStruct())
