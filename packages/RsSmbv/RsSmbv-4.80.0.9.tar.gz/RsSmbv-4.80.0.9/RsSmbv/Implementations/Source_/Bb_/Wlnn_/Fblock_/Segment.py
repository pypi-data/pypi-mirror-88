from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Segment:
	"""Segment commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("segment", core, parent)

	def set(self, segment: enums.WlannFbSegment, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SEGMent \n
		Selects one of the two segments in VHT-80+80 MHz mode with transmission bandwidth 80 MHz or 160 MHz. Both segments can
		only be generated with bandwidth 160 MHz. This parameter applies to VHT-80+80 MHz Tx mode only. \n
			:param segment: SEG0| SEG1| BOTH
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(segment, enums.WlannFbSegment)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SEGMent {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbSegment:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SEGMent \n
		Selects one of the two segments in VHT-80+80 MHz mode with transmission bandwidth 80 MHz or 160 MHz. Both segments can
		only be generated with bandwidth 160 MHz. This parameter applies to VHT-80+80 MHz Tx mode only. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: segment: SEG0| SEG1| BOTH"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SEGMent?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbSegment)
