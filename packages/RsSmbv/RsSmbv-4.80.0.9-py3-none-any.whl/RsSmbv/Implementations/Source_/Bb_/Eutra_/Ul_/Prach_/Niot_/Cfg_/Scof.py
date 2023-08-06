from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scof:
	"""Scof commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scof", core, parent)

	def set(self, subcarrier_offse: enums.EutraPracNbiotSubcarrierOffset, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:SCOF \n
		Sets the NPRACH subcarrier offset. \n
			:param subcarrier_offse: 0| 2| 12| 18| 24| 34| 36 | 6| 42| 48| 54| 60| 72| 78| 84| 90| 102| 108
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')"""
		param = Conversions.enum_scalar_to_str(subcarrier_offse, enums.EutraPracNbiotSubcarrierOffset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:SCOF {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraPracNbiotSubcarrierOffset:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:SCOF \n
		Sets the NPRACH subcarrier offset. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')
			:return: subcarrier_offse: 0| 2| 12| 18| 24| 34| 36 | 6| 42| 48| 54| 60| 72| 78| 84| 90| 102| 108"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:SCOF?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPracNbiotSubcarrierOffset)
