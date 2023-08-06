from typing import List

from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal.Types import DataType
from ............Internal.StructBase import StructBase
from ............Internal.ArgStruct import ArgStruct
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbpAtt:
	"""RbpAtt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbpAtt", core, parent)

	# noinspection PyTypeChecker
	class RbpAttStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: 275 bits
			- Bitcount: int: integer Range: 275 to 275"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: RbpAttStruct, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, rateSetting=repcap.RateSetting.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:RATM:RS<GR>:RBPatt \n
		Sets the resource block level bitmap pattern directly, alternatively to loading a data list with the command method
		RsSmbv.Source.Bb.Nr5G.Ubwp.User.Cell.Dl.Bwp.Ratm.Rs.Rbdlist.set. \n
			:param structure: for set value, see the help for RbpAttStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSetting: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		rateSetting_cmd_val = self._base.get_repcap_cmd_value(rateSetting, repcap.RateSetting)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:RATM:RS{rateSetting_cmd_val}:RBPatt', structure)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, rateSetting=repcap.RateSetting.Default) -> RbpAttStruct:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:RATM:RS<GR>:RBPatt \n
		Sets the resource block level bitmap pattern directly, alternatively to loading a data list with the command method
		RsSmbv.Source.Bb.Nr5G.Ubwp.User.Cell.Dl.Bwp.Ratm.Rs.Rbdlist.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSetting: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')
			:return: structure: for return value, see the help for RbpAttStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		rateSetting_cmd_val = self._base.get_repcap_cmd_value(rateSetting, repcap.RateSetting)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:RATM:RS{rateSetting_cmd_val}:RBPatt?', self.__class__.RbpAttStruct())
