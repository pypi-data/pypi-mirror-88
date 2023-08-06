from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tbal:
	"""Tbal commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tbal", core, parent)

	def set(self, tbs_alt_index: enums.EutraMcsTable, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:CELL<ST>:TBAL \n
		Sets the which of the transport block size (TBS) tables defined in is used. \n
			:param tbs_alt_index: 0| OFF| T1| 1| ON| T2| T3| T4 0|OFF|T1 ='TBS Alt. Index = 0' 1|ON|T2 = 'TBS Alt. Index = 1' T3 = 'TBS Alt. Index = 2' T3 = 'TBS Alt. Index = 3'
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(tbs_alt_index, enums.EutraMcsTable)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:CELL{stream_cmd_val}:TBAL {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.EutraMcsTable:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:CELL<ST>:TBAL \n
		Sets the which of the transport block size (TBS) tables defined in is used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: tbs_alt_index: 0| OFF| T1| 1| ON| T2| T3| T4 0|OFF|T1 ='TBS Alt. Index = 0' 1|ON|T2 = 'TBS Alt. Index = 1' T3 = 'TBS Alt. Index = 2' T3 = 'TBS Alt. Index = 3'"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:CELL{stream_cmd_val}:TBAL?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMcsTable)
