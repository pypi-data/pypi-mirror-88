from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pformat:
	"""Pformat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pformat", core, parent)

	def set(self, ppdu_format: enums.WlannFbPpduFormat, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:PFORmat \n
		Sets the PPDU format. \n
			:param ppdu_format: SU| MU| SUEXt| TRIG SU HE SU (single-user) carries a single PSDU. The HE Signal A (HE-SIG-A) field is not repeated. MU HE MU (multi-user) carries multiple PSDUs to one or more users. SUEXt Carries a single PSDU. The HE-SIG-A field is repeated.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(ppdu_format, enums.WlannFbPpduFormat)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PFORmat {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbPpduFormat:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:PFORmat \n
		Sets the PPDU format. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ppdu_format: SU| MU| SUEXt| TRIG SU HE SU (single-user) carries a single PSDU. The HE Signal A (HE-SIG-A) field is not repeated. MU HE MU (multi-user) carries multiple PSDUs to one or more users. SUEXt Carries a single PSDU. The HE-SIG-A field is repeated."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPpduFormat)
