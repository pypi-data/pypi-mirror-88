from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrPeriod:
	"""SrPeriod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srPeriod", core, parent)

	def set(self, sfn_rest_period: enums.EutraPbchSfnRestPeriod, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CCODing:SRPeriod \n
		Determines the time span after which the SFN (System Frame Number) restarts. \n
			:param sfn_rest_period: PERSlength PERSlength = SFN restart period to the ARB sequence length
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(sfn_rest_period, enums.EutraPbchSfnRestPeriod)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CCODing:SRPeriod {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraPbchSfnRestPeriod:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CCODing:SRPeriod \n
		Determines the time span after which the SFN (System Frame Number) restarts. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: sfn_rest_period: PERSlength PERSlength = SFN restart period to the ARB sequence length"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CCODing:SRPeriod?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPbchSfnRestPeriod)
