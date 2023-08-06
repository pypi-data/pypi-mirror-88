from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def set(self, frequency: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier<CH>:FREQuency \n
		Sets or indicates the carrier frequency, depending on the selected carrier frequency mode. \n
			:param frequency: integer Range: depends on the installed options E.g. -60 MHz to +60 MHz (base unit)
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.decimal_value_to_str(frequency)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier{channel_cmd_val}:FREQuency {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier<CH>:FREQuency \n
		Sets or indicates the carrier frequency, depending on the selected carrier frequency mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: frequency: integer Range: depends on the installed options E.g. -60 MHz to +60 MHz (base unit)"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier{channel_cmd_val}:FREQuency?')
		return Conversions.str_to_int(response)
