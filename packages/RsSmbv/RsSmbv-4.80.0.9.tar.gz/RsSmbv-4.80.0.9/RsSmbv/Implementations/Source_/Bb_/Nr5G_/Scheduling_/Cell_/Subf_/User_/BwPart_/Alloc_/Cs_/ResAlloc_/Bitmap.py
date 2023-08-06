from typing import List

from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.Types import DataType
from .............Internal.StructBase import StructBase
from .............Internal.ArgStruct import ArgStruct
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bitmap:
	"""Bitmap commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bitmap", core, parent)

	# noinspection PyTypeChecker
	class BitmapStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Res_Alloc_Bit_Map: List[str]: 45 bits
			- Bit_Count: int: integer Range: 45 to 45"""
		__meta_args_list = [
			ArgStruct('Res_Alloc_Bit_Map', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Res_Alloc_Bit_Map: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: BitmapStruct, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:RESalloc:BITMap \n
		If method RsSmbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.Cs.ResAlloc.State.set 1, sets the CORESET
		allocation in the frequency domain. \n
			:param structure: for set value, see the help for BitmapStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:RESalloc:BITMap', structure)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> BitmapStruct:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:RESalloc:BITMap \n
		If method RsSmbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.Cs.ResAlloc.State.set 1, sets the CORESET
		allocation in the frequency domain. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: structure: for return value, see the help for BitmapStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:RESalloc:BITMap?', self.__class__.BitmapStruct())
