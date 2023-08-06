from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Privacy:
	"""Privacy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("privacy", core, parent)

	def set(self, privacy: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:PRIVacy \n
		Informs the associated stations if encryption is required for all data frames. \n
			:param privacy: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(privacy)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:PRIVacy {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:PRIVacy \n
		Informs the associated stations if encryption is required for all data frames. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: privacy: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:PRIVacy?')
		return Conversions.str_to_bool(response)
