from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deviation", core, parent)

	def set(self, deviation: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:FM:INTernal<CH>:DEViation \n
		No command help available \n
			:param deviation: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fm')"""
		param = Conversions.decimal_value_to_str(deviation)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:FM:INTernal{channel_cmd_val}:DEViation {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:FM:INTernal<CH>:DEViation \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fm')
			:return: deviation: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FM:INTernal{channel_cmd_val}:DEViation?')
		return Conversions.str_to_float(response)
