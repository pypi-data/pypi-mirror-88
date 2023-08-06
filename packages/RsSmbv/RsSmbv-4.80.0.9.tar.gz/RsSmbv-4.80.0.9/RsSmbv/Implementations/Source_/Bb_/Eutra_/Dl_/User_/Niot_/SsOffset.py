from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SsOffset:
	"""SsOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssOffset", core, parent)

	def set(self, search_space_offs: enums.EutraNbiotSearchSpaceOffset, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:NIOT:SSOFfset \n
		Shifts the search space start. \n
			:param search_space_offs: O0| O1_8| O1_4| O3_8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(search_space_offs, enums.EutraNbiotSearchSpaceOffset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:NIOT:SSOFfset {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraNbiotSearchSpaceOffset:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:NIOT:SSOFfset \n
		Shifts the search space start. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: search_space_offs: O0| O1_8| O1_4| O3_8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:NIOT:SSOFfset?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotSearchSpaceOffset)
