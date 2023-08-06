from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offset", core, parent)

	def set(self, freq_offs: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:NOTCh<CH>:FREQuency:OFFSet \n
		No command help available \n
			:param freq_offs: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')"""
		param = Conversions.decimal_value_to_str(freq_offs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:NOTCh{channel_cmd_val}:FREQuency:OFFSet {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:OFDM:NOTCh<CH>:FREQuency:OFFSet \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: freq_offs: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:NOTCh{channel_cmd_val}:FREQuency:OFFSet?')
		return Conversions.str_to_int(response)
