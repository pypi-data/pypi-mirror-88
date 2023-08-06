from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TbSize:
	"""TbSize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tbSize", core, parent)

	def set(self, tb_size: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:DCCH<CH>:TBSize \n
		Sets the size of the transport block at the channel coding input. \n
			:param tb_size: integer Range: 0 to 4096
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dcch')"""
		param = Conversions.decimal_value_to_str(tb_size)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:DCCH{channel_cmd_val}:TBSize {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:DCCH<CH>:TBSize \n
		Sets the size of the transport block at the channel coding input. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dcch')
			:return: tb_size: integer Range: 0 to 4096"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:DCCH{channel_cmd_val}:TBSize?')
		return Conversions.str_to_int(response)
