from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbNumber:
	"""RbNumber commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbNumber", core, parent)

	def set(self, user_alloc_rbn_um: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:RBNumber \n
		Sets the number of resource blocks (RB) the allocation spans. \n
			:param user_alloc_rbn_um: integer CORESET allocations span always a multiple of 6 resource blocks. Thus, only values that are multiple of 6 are allowed for these allocations. The number of resource blocks that are available for PUSCH depends on whether the transform precoding is enabled or not (that is if DFT-s-OFDM is applied) , see BB:NR5G:SCHed:CELLch0:SUBFst0:USERdir0:BWPartgr0:ALLocuser0:TPSTate. Query the number of resource blocks used by PRACH with the command method RsSmbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.Prach.RbNumber.get_. Range: 20 to 275
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.decimal_value_to_str(user_alloc_rbn_um)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:RBNumber {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:RBNumber \n
		Sets the number of resource blocks (RB) the allocation spans. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: user_alloc_rbn_um: integer CORESET allocations span always a multiple of 6 resource blocks. Thus, only values that are multiple of 6 are allowed for these allocations. The number of resource blocks that are available for PUSCH depends on whether the transform precoding is enabled or not (that is if DFT-s-OFDM is applied) , see BB:NR5G:SCHed:CELLch0:SUBFst0:USERdir0:BWPartgr0:ALLocuser0:TPSTate. Query the number of resource blocks used by PRACH with the command method RsSmbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.Prach.RbNumber.get_. Range: 20 to 275"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:RBNumber?')
		return Conversions.str_to_int(response)
