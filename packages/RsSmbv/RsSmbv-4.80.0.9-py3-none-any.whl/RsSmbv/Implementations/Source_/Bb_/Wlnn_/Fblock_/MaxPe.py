from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaxPe:
	"""MaxPe commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maxPe", core, parent)

	def set(self, max_pe_duration: enums.WlannFbPpduPeDuraion, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAXPe \n
		Sets the maximum packet extension (PE) duration. \n
			:param max_pe_duration: PE0| PE8| PE16 PE0: 0 us PE8: 8 us PE16: 16 us
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(max_pe_duration, enums.WlannFbPpduPeDuraion)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAXPe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbPpduPeDuraion:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:MAXPe \n
		Sets the maximum packet extension (PE) duration. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: max_pe_duration: PE0| PE8| PE16 PE0: 0 us PE8: 8 us PE16: 16 us"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAXPe?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPpduPeDuraion)
