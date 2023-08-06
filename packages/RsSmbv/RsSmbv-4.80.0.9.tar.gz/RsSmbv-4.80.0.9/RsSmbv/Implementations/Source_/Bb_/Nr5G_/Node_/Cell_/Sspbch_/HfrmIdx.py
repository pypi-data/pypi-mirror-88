from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HfrmIdx:
	"""HfrmIdx commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hfrmIdx", core, parent)

	def set(self, half_frame_idx: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:HFRMidx \n
		Defines in which half-frame of the time plan the first SS/PBCH burst occasion is located. The 'Half Frame Index' value
		depends on the configured 'Burst Set Periodicity'. The default value is 0, it locates the first SS/PBCH occasion in the
		first half-frame. If you set the value to 1, the first SS/PBCH occasion is in the second half-frame and so forth. \n
			:param half_frame_idx: integer Range: 0 to 31
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')"""
		param = Conversions.decimal_value_to_str(half_frame_idx)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:HFRMidx {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:HFRMidx \n
		Defines in which half-frame of the time plan the first SS/PBCH burst occasion is located. The 'Half Frame Index' value
		depends on the configured 'Burst Set Periodicity'. The default value is 0, it locates the first SS/PBCH occasion in the
		first half-frame. If you set the value to 1, the first SS/PBCH occasion is in the second half-frame and so forth. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:return: half_frame_idx: integer Range: 0 to 31"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:HFRMidx?')
		return Conversions.str_to_int(response)
