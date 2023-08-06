from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UeMode:
	"""UeMode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ueMode", core, parent)

	def set(self, ue_mode: enums.EutraUeMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH>:UEMode \n
		Sets the DCI field mode and defines if the DCI format 6-1A/B is used for PDSCH or PRACH. \n
			:param ue_mode: STD| PRACh
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(ue_mode, enums.EutraUeMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{channel_cmd_val}:UEMode {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraUeMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:DCI:ALLoc<CH>:UEMode \n
		Sets the DCI field mode and defines if the DCI format 6-1A/B is used for PDSCH or PRACH. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: ue_mode: STD| PRACh"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:DCI:ALLoc{channel_cmd_val}:UEMode?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUeMode)
