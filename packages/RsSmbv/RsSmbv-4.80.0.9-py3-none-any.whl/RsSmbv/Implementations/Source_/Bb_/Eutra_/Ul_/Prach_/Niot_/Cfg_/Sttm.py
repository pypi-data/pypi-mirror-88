from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sttm:
	"""Sttm commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sttm", core, parent)

	def set(self, start_time: enums.EutraPracNbiotStartTimeMs, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:STTM \n
		Sets the start time of the specific NPRACH configuration. \n
			:param start_time: 8| 16| 64| 128| 32| 256| 512| 1024 | 10| 20| 40| 80| 160| 320| 640| 1280| 2560| 5120
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')"""
		param = Conversions.enum_scalar_to_str(start_time, enums.EutraPracNbiotStartTimeMs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:STTM {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraPracNbiotStartTimeMs:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:STTM \n
		Sets the start time of the specific NPRACH configuration. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')
			:return: start_time: 8| 16| 64| 128| 32| 256| 512| 1024 | 10| 20| 40| 80| 160| 320| 640| 1280| 2560| 5120"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:STTM?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPracNbiotStartTimeMs)
