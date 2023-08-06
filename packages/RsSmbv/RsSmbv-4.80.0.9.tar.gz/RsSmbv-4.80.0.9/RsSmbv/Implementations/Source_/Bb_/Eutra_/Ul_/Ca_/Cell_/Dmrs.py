from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmrs:
	"""Dmrs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmrs", core, parent)

	def set(self, ulca_n_1_dmrs: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:CA:CELL<CH>:DMRS \n
		Sets the parameter n(1) _DMRS per component carrier. \n
			:param ulca_n_1_dmrs: integer Range: 0 to 11
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(ulca_n_1_dmrs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:CELL{channel_cmd_val}:DMRS {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:CA:CELL<CH>:DMRS \n
		Sets the parameter n(1) _DMRS per component carrier. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: ulca_n_1_dmrs: integer Range: 0 to 11"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:CELL{channel_cmd_val}:DMRS?')
		return Conversions.str_to_int(response)
