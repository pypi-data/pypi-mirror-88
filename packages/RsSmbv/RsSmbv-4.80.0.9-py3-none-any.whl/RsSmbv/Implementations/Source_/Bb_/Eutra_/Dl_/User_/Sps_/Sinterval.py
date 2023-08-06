from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sinterval:
	"""Sinterval commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sinterval", core, parent)

	def set(self, user_sps_int: enums.EutraSpsInt, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SPS:SINTerval \n
		Defines the SPS interval. \n
			:param user_sps_int: S10| S20| S32| S40| S64| S80| S128| S160| S320| S640
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(user_sps_int, enums.EutraSpsInt)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:SPS:SINTerval {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraSpsInt:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SPS:SINTerval \n
		Defines the SPS interval. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: user_sps_int: S10| S20| S32| S40| S64| S80| S128| S160| S320| S640"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:SPS:SINTerval?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSpsInt)
