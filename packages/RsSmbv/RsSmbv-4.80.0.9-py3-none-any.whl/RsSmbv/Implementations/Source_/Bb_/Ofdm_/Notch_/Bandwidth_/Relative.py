from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Relative:
	"""Relative commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("relative", core, parent)

	def set(self, bw_pct: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:NOTCh<CH>:BWIDth:RELative \n
		No command help available \n
			:param bw_pct: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')"""
		param = Conversions.decimal_value_to_str(bw_pct)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:NOTCh{channel_cmd_val}:BWIDth:RELative {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:OFDM:NOTCh<CH>:BWIDth:RELative \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: bw_pct: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:NOTCh{channel_cmd_val}:BWIDth:RELative?')
		return Conversions.str_to_float(response)
