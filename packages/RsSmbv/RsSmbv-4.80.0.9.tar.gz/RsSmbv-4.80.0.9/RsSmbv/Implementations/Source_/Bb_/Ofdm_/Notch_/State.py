from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, notch_val_enable: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:NOTCh<CH>:STATe \n
		No command help available \n
			:param notch_val_enable: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')"""
		param = Conversions.bool_to_str(notch_val_enable)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:NOTCh{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:OFDM:NOTCh<CH>:STATe \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: notch_val_enable: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:NOTCh{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
