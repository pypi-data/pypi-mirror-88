from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Periodicity:
	"""Periodicity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("periodicity", core, parent)

	def set(self, drs_periodicity: enums.EutraDsPeriod, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:PERiodicity \n
		Sets the DRS periodictity. \n
			:param drs_periodicity: P40| P80| P160
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(drs_periodicity, enums.EutraDsPeriod)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:PERiodicity {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraDsPeriod:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:PERiodicity \n
		Sets the DRS periodictity. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: drs_periodicity: P40| P80| P160"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:PERiodicity?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDsPeriod)
