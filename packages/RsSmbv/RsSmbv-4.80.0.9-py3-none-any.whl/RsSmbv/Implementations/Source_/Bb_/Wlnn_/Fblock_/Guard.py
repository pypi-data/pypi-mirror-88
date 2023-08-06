from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Guard:
	"""Guard commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("guard", core, parent)

	def set(self, guard: enums.WlannFbGuard, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:GUARd \n
		Selects which guard interval is used for the OFDM guard. In physical mode green field or legacy, only long guard
		intervals are possible. In this case, the field is read-only. GD08, GD16 and GD32 are available only for the IEEE 802.
		11ax standard. \n
			:param guard: SHORt| LONG| GD08| GD16| GD32
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(guard, enums.WlannFbGuard)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:GUARd {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbGuard:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:GUARd \n
		Selects which guard interval is used for the OFDM guard. In physical mode green field or legacy, only long guard
		intervals are possible. In this case, the field is read-only. GD08, GD16 and GD32 are available only for the IEEE 802.
		11ax standard. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: guard: SHORt| LONG| GD08| GD16| GD32"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:GUARd?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbGuard)
