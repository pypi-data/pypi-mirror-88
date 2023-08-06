from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cw:
	"""Cw commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cw", core, parent)

	def set(self, cw_frequency: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:FREQuency:CW \n
		Sets the frequency of the CW interfering signal. \n
			:param cw_frequency: integer Range: 1E9 to 2E9, Unit: Hz
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(cw_frequency)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:FREQuency:CW {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:FREQuency:CW \n
		Sets the frequency of the CW interfering signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: cw_frequency: integer Range: 1E9 to 2E9, Unit: Hz"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:FREQuency:CW?')
		return Conversions.str_to_int(response)
