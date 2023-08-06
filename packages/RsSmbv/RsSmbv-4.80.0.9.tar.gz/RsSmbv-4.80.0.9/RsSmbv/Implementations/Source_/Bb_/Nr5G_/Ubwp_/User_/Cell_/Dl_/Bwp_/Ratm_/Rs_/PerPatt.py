from typing import List

from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal.Types import DataType
from ............Internal.StructBase import StructBase
from ............Internal.ArgStruct import ArgStruct
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PerPatt:
	"""PerPatt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("perPatt", core, parent)

	# noinspection PyTypeChecker
	class PerPattStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Rate_Mat_Perd_Patt: List[str]: 40 bits
			- Bit_Count: int: integer Range: 1 to 40"""
		__meta_args_list = [
			ArgStruct('Rate_Mat_Perd_Patt', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rate_Mat_Perd_Patt: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: PerPattStruct, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, rateSetting=repcap.RateSetting.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:RATM:RS<GR>:PERPatt \n
		Sets the periodicity in a pattern form. \n
			:param structure: for set value, see the help for PerPattStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSetting: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		rateSetting_cmd_val = self._base.get_repcap_cmd_value(rateSetting, repcap.RateSetting)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:RATM:RS{rateSetting_cmd_val}:PERPatt', structure)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, rateSetting=repcap.RateSetting.Default) -> PerPattStruct:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:RATM:RS<GR>:PERPatt \n
		Sets the periodicity in a pattern form. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSetting: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')
			:return: structure: for return value, see the help for PerPattStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		rateSetting_cmd_val = self._base.get_repcap_cmd_value(rateSetting, repcap.RateSetting)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:RATM:RS{rateSetting_cmd_val}:PERPatt?', self.__class__.PerPattStruct())
