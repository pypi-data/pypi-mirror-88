from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Encoder:
	"""Encoder commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("encoder", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> enums.WlannFbEncoder:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:CODing:ENCoder \n
		Queries the number of encoders to be used. This value depends on the data rate. For data rate ≤ 300 Mps, this value is 1.
		Otherwise the number of encoders is 2. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: encoder: E1| E2| E3| E6| E7| E8| E9| E12| E4| E5| E10| E11"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:CODing:ENCoder?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbEncoder)
