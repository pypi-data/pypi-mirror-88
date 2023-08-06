from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adelay:
	"""Adelay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adelay", core, parent)

	def set(self, additional_delay: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:HPPS:ADELay \n
		Sets an additional delay for the high-precision PPS marker signal. \n
			:param additional_delay: float Range: 0 to 10E-6
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(additional_delay)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{channel_cmd_val}:HPPS:ADELay {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:HPPS:ADELay \n
		Sets an additional delay for the high-precision PPS marker signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: additional_delay: float Range: 0 to 10E-6"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{channel_cmd_val}:HPPS:ADELay?')
		return Conversions.str_to_float(response)
