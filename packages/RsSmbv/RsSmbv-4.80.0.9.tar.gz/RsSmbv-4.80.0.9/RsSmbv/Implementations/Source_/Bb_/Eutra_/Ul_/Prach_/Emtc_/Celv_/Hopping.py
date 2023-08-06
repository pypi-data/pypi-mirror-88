from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hopping:
	"""Hopping commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hopping", core, parent)

	def set(self, hopping: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:CELV<CH>:HOPPing \n
		Enables frequency hopping. \n
			:param hopping: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Celv')"""
		param = Conversions.bool_to_str(hopping)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:CELV{channel_cmd_val}:HOPPing {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:CELV<CH>:HOPPing \n
		Enables frequency hopping. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Celv')
			:return: hopping: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:CELV{channel_cmd_val}:HOPPing?')
		return Conversions.str_to_bool(response)
