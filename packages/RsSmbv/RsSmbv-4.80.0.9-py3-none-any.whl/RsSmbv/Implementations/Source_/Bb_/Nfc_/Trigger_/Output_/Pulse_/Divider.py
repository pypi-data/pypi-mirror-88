from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Divider:
	"""Divider commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("divider", core, parent)

	def set(self, divider: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:TRIGger:OUTPut<CH>:PULSe:DIVider \n
		Sets the divider for the pulsed marker signal. \n
			:param divider: integer Range: 2 to 1024
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(divider)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:TRIGger:OUTPut{channel_cmd_val}:PULSe:DIVider {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NFC:TRIGger:OUTPut<CH>:PULSe:DIVider \n
		Sets the divider for the pulsed marker signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: divider: integer Range: 2 to 1024"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:TRIGger:OUTPut{channel_cmd_val}:PULSe:DIVider?')
		return Conversions.str_to_int(response)
