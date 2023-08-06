from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Block:
	"""Block commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Block, default value after init: Block.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("block", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_block_get', 'repcap_block_set', repcap.Block.Nr1)

	def clone(self) -> 'Block':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Block(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_block_set(self, enum_value: repcap.Block) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Block.Default
		Default value after init: Block.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_block_get(self) -> repcap.Block:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, block_param: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, block=repcap.Block.Default) -> None:
		"""[SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:UMT:DATA<CH>:BLOCk<USER> \n
		No command help available \n
			:param block_param: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Data')
			:param block: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')"""
		param = Conversions.decimal_value_to_str(block_param)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		block_cmd_val = self._base.get_repcap_cmd_value(block, repcap.Block)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:UMT:DATA{channel_cmd_val}:BLOCk{block_cmd_val} {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, block=repcap.Block.Default) -> int:
		"""[SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:UMT:DATA<CH>:BLOCk<USER> \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Data')
			:param block: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Block')
			:return: block_param: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		block_cmd_val = self._base.get_repcap_cmd_value(block, repcap.Block)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:UMT:DATA{channel_cmd_val}:BLOCk{block_cmd_val}?')
		return Conversions.str_to_int(response)
