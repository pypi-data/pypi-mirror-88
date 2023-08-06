from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcs:
	"""Mcs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcs", core, parent)

	def set(self, mcs_table: enums.EutraMcsTable, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:CELL<ST>:MCS \n
		Defines which of the tables defined in is used to specify the used modulation and coding scheme. \n
			:param mcs_table: 0| OFF| T1| 1| ON| T2| T3| T4 0|OFF|T1 Table 7.1.7.1-1 1|ON|T2 Table 7.1.7.1-1A T3 Table 7.1.7.1-1B T4 Table 7.1.7.1-1C
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(mcs_table, enums.EutraMcsTable)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:CELL{stream_cmd_val}:MCS {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.EutraMcsTable:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:CELL<ST>:MCS \n
		Defines which of the tables defined in is used to specify the used modulation and coding scheme. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: mcs_table: 0| OFF| T1| 1| ON| T2| T3| T4 0|OFF|T1 Table 7.1.7.1-1 1|ON|T2 Table 7.1.7.1-1A T3 Table 7.1.7.1-1B T4 Table 7.1.7.1-1C"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:CELL{stream_cmd_val}:MCS?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMcsTable)
