from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uindex:
	"""Uindex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uindex", core, parent)

	def set(self, uind: enums.WlannFbUserIdx, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:UINDex \n
		Defines the currently generated user. In activated Multi User MIMO only, one user can be generated at a time.
		This parameter selects the generated one out of four available users. \n
			:param uind: UIDX0| UIDX1| UIDX2| UIDX3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(uind, enums.WlannFbUserIdx)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:UINDex {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbUserIdx:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:UINDex \n
		Defines the currently generated user. In activated Multi User MIMO only, one user can be generated at a time.
		This parameter selects the generated one out of four available users. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: uind: UIDX0| UIDX1| UIDX2| UIDX3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:UINDex?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbUserIdx)
