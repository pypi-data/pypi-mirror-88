from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def set(self, scma_layer_user: enums.C5GscmaUser, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:SCMA:LAYer<ST>:USER \n
		Maps the users to the layers. \n
			:param scma_layer_user: USER0| USER1| USER2| USER3| USER4| USER5
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')"""
		param = Conversions.enum_scalar_to_str(scma_layer_user, enums.C5GscmaUser)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:SCMA:LAYer{stream_cmd_val}:USER {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.C5GscmaUser:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:SCMA:LAYer<ST>:USER \n
		Maps the users to the layers. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: scma_layer_user: USER0| USER1| USER2| USER3| USER4| USER5"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:SCMA:LAYer{stream_cmd_val}:USER?')
		return Conversions.str_to_scalar_enum(response, enums.C5GscmaUser)
