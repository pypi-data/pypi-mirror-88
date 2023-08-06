from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pointa:
	"""Pointa commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pointa", core, parent)

	def set(self, carrier_point_a: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:TXBW:POINta \n
		Sets the frequency offset between the reference Point A and the center carrier frequency. \n
			:param carrier_point_a: float Range: -50e6 to 0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(carrier_point_a)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:TXBW:POINta {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:TXBW:POINta \n
		Sets the frequency offset between the reference Point A and the center carrier frequency. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: carrier_point_a: float Range: -50e6 to 0"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:TXBW:POINta?')
		return Conversions.str_to_float(response)
