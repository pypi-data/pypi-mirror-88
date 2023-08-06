from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ncfg:
	"""Ncfg commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ncfg", core, parent)

	def set(self, number_of_configs: enums.EutraCsiRsNumCfg, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:NCFG \n
		Sets the number of CSI-RS configurations. \n
			:param number_of_configs: 1| 2| 3| 4| 5| 7
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(number_of_configs, enums.EutraCsiRsNumCfg)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:NCFG {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraCsiRsNumCfg:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:NCFG \n
		Sets the number of CSI-RS configurations. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: number_of_configs: 1| 2| 3| 4| 5| 7"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:NCFG?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCsiRsNumCfg)
