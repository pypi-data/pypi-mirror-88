from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccd:
	"""Ccd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccd", core, parent)

	def set(self, cyc_del_div: enums.EutraDlpRecCycDelDiv, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:PRECoding:CCD \n
		Sets the cyclic delay diversity for the selected allocation. \n
			:param cyc_del_div: NOCDd| LADelay
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(cyc_del_div, enums.EutraDlpRecCycDelDiv)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:PRECoding:CCD {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraDlpRecCycDelDiv:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:PRECoding:CCD \n
		Sets the cyclic delay diversity for the selected allocation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: cyc_del_div: NOCDd| LADelay"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:PRECoding:CCD?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDlpRecCycDelDiv)
