from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ontime:
	"""Ontime commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ontime", core, parent)

	def set(self, on_time: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:TRIGger:OUTPut<CH>:ONTime \n
		Sets the number of chips during which the marker output is on or off. \n
			:param on_time: integer Range: 1 to 16777215, Unit: chip
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(on_time)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:TRIGger:OUTPut{channel_cmd_val}:ONTime {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:TRIGger:OUTPut<CH>:ONTime \n
		Sets the number of chips during which the marker output is on or off. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: on_time: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:TRIGger:OUTPut{channel_cmd_val}:ONTime?')
		return Conversions.str_to_int(response)
