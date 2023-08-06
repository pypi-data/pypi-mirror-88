from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Perd:
	"""Perd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("perd", core, parent)

	def set(self, periodicity: enums.EutraPracNbiotPeriodicity, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:PERD \n
		Sets NPRACH periodicity. \n
			:param periodicity: 40| 80| 160| 240| 320| 640| 1280| 2560 | 5120| 10240
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')"""
		param = Conversions.enum_scalar_to_str(periodicity, enums.EutraPracNbiotPeriodicity)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:PERD {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraPracNbiotPeriodicity:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:PERD \n
		Sets NPRACH periodicity. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')
			:return: periodicity: 40| 80| 160| 240| 320| 640| 1280| 2560 | 5120| 10240"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:PERD?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPracNbiotPeriodicity)
