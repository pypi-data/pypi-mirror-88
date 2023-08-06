from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McsMode:
	"""McsMode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcsMode", core, parent)

	def set(self, mcs_mode: enums.EutraAsEqMcsMode, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:MCSMode \n
		Sets how the Modulation and Coding Scheme is configured. \n
			:param mcs_mode: MANual| FIXed| TCR
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		param = Conversions.enum_scalar_to_str(mcs_mode, enums.EutraAsEqMcsMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:MCSMode {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> enums.EutraAsEqMcsMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:MCSMode \n
		Sets how the Modulation and Coding Scheme is configured. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1
			:return: mcs_mode: MANual| FIXed| TCR"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:MCSMode?')
		return Conversions.str_to_scalar_enum(response, enums.EutraAsEqMcsMode)
