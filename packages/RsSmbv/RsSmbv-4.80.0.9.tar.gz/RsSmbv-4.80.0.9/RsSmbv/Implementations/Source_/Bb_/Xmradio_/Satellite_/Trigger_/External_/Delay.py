from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def set(self, delay: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:XMRadio:SATellite:TRIGger:[EXTernal<CH>]:DELay \n
		No command help available \n
			:param delay: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')"""
		param = Conversions.decimal_value_to_str(delay)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:SATellite:TRIGger:EXTernal{channel_cmd_val}:DELay {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:XMRadio:SATellite:TRIGger:[EXTernal<CH>]:DELay \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')
			:return: delay: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:XMRadio:SATellite:TRIGger:EXTernal{channel_cmd_val}:DELay?')
		return Conversions.str_to_float(response)
