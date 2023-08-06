from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Foffset:
	"""Foffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("foffset", core, parent)

	def set(self, frequency_offset: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:CELV<CH>:FOFFset \n
		Sets a frequency offset in terms of resource blocks. \n
			:param frequency_offset: integer Range: 0 to 94
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Celv')"""
		param = Conversions.decimal_value_to_str(frequency_offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:CELV{channel_cmd_val}:FOFFset {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:CELV<CH>:FOFFset \n
		Sets a frequency offset in terms of resource blocks. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Celv')
			:return: frequency_offset: integer Range: 0 to 94"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:CELV{channel_cmd_val}:FOFFset?')
		return Conversions.str_to_int(response)
