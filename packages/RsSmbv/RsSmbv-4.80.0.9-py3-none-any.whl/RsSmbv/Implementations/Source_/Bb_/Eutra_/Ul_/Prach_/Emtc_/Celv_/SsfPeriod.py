from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SsfPeriod:
	"""SsfPeriod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssfPeriod", core, parent)

	def set(self, start_sf_period: enums.IdEutraEmtcPrachStartingSfPeriod, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:CELV<CH>:SSFPeriod \n
		Sets the starting subframe periodicity. \n
			:param start_sf_period: NONE| 4| 2| 8| 16| 32| 64| 128| 256
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Celv')"""
		param = Conversions.enum_scalar_to_str(start_sf_period, enums.IdEutraEmtcPrachStartingSfPeriod)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:CELV{channel_cmd_val}:SSFPeriod {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.IdEutraEmtcPrachStartingSfPeriod:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:CELV<CH>:SSFPeriod \n
		Sets the starting subframe periodicity. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Celv')
			:return: start_sf_period: NONE| 4| 2| 8| 16| 32| 64| 128| 256"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:CELV{channel_cmd_val}:SSFPeriod?')
		return Conversions.str_to_scalar_enum(response, enums.IdEutraEmtcPrachStartingSfPeriod)
