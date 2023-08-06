from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Taoffset:
	"""Taoffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("taoffset", core, parent)

	def set(self, timing_adj_offset: enums.TimingAdjustmentOffsetAll, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:TAOFfset \n
		Sets an offset (NTA offset) to the timing advance value for UL/DL switching synchronization as specified in . The NTA
		offset values can be set as specified in . \n
			:param timing_adj_offset: N0| N13792| N25600| N39936
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(timing_adj_offset, enums.TimingAdjustmentOffsetAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:TAOFfset {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.TimingAdjustmentOffsetAll:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:TAOFfset \n
		Sets an offset (NTA offset) to the timing advance value for UL/DL switching synchronization as specified in . The NTA
		offset values can be set as specified in . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: timing_adj_offset: N0| N13792| N25600| N39936"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:TAOFfset?')
		return Conversions.str_to_scalar_enum(response, enums.TimingAdjustmentOffsetAll)
