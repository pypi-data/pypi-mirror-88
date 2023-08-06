from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pa:
	"""Pa commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pa", core, parent)

	def set(self, power: enums.EutraPdscPowA, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:PA \n
		Sets PDSCH power factor according to , chapter 5.2. \n
			:param power: -6.02| -4.77| -3.01| -1.77| 0.97| 2.04| 3.01| 0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(power, enums.EutraPdscPowA)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:PA {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraPdscPowA:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:PA \n
		Sets PDSCH power factor according to , chapter 5.2. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: power: -6.02| -4.77| -3.01| -1.77| 0.97| 2.04| 3.01| 0"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:PA?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPdscPowA)
