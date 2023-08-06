from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nap:
	"""Nap commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nap", core, parent)

	def set(self, csi_rs_num_ap: enums.EutraCsiRsNumAp, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:NAP \n
		Defines the number of antenna ports the CSI-RS are transmitted on. \n
			:param csi_rs_num_ap: AP1| AP2| AP4| AP8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(csi_rs_num_ap, enums.EutraCsiRsNumAp)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:NAP {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraCsiRsNumAp:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:NAP \n
		Defines the number of antenna ports the CSI-RS are transmitted on. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: csi_rs_num_ap: AP1| AP2| AP4| AP8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:NAP?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCsiRsNumAp)
