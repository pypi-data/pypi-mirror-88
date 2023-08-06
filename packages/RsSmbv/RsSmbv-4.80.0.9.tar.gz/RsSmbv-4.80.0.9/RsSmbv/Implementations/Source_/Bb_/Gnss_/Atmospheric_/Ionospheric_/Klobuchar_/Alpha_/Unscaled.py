from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, alpha_unscaled: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:KLOBuchar:ALPHa<CH>:UNSCaled \n
		Sets the klobuchar parameters alpha_0 to alpha_3. \n
			:param alpha_unscaled: float Range: dynamic
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alpha')"""
		param = Conversions.decimal_value_to_str(alpha_unscaled)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:KLOBuchar:ALPHa{channel_cmd_val}:UNSCaled {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:KLOBuchar:ALPHa<CH>:UNSCaled \n
		Sets the klobuchar parameters alpha_0 to alpha_3. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alpha')
			:return: alpha_unscaled: float Range: dynamic"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:KLOBuchar:ALPHa{channel_cmd_val}:UNSCaled?')
		return Conversions.str_to_float(response)
