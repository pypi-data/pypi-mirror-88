from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tc:
	"""Tc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tc", core, parent)

	def set(self, tc_rnti: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:RNTI:TC \n
		Sets the TC-RNTI of the user. It is a unique UE identification used as an identifier of the RRC connection and for
		scheduling with a temporary cell. \n
			:param tc_rnti: integer Range: 1 to 65519
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(tc_rnti)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:RNTI:TC {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:RNTI:TC \n
		Sets the TC-RNTI of the user. It is a unique UE identification used as an identifier of the RRC connection and for
		scheduling with a temporary cell. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: tc_rnti: integer Range: 1 to 65519"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:RNTI:TC?')
		return Conversions.str_to_int(response)
