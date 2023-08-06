from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.IdEutraNbiotMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:MODE \n
		Sets the operating mode. \n
			:param mode: INBD| ALON| GBD
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.enum_scalar_to_str(mode, enums.IdEutraNbiotMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.IdEutraNbiotMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:MODE \n
		Sets the operating mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: mode: INBD| ALON| GBD"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.IdEutraNbiotMode)
