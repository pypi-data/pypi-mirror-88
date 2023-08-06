from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def set(self, frequency: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:DOWN:MC:CARRier<CH>:FREQuency \n
		Sets the center frequency of the carrier in MHz. In some cases, not all center frequencies are defined by the selected
		band class. In case a non-existing frequency is input, the next available frequency is used. \n
			:param frequency: float Range: 100 to 3000
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.decimal_value_to_str(frequency)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:DOWN:MC:CARRier{channel_cmd_val}:FREQuency {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:EVDO:DOWN:MC:CARRier<CH>:FREQuency \n
		Sets the center frequency of the carrier in MHz. In some cases, not all center frequencies are defined by the selected
		band class. In case a non-existing frequency is input, the next available frequency is used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: frequency: float Range: 100 to 3000"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:DOWN:MC:CARRier{channel_cmd_val}:FREQuency?')
		return Conversions.str_to_float(response)
