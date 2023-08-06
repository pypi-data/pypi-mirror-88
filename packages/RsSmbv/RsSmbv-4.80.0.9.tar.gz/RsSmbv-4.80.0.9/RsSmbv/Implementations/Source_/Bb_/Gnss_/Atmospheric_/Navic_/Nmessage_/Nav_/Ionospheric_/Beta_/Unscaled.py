from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, beta_unscaled: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:NAVic:[NMESsage]:[NAV]:IONospheric:BETA<CH>:UNSCaled \n
		Sets the parameters beta_0 to beta_3 of the satellite's navigation message. \n
			:param beta_unscaled: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beta')"""
		param = Conversions.decimal_value_to_str(beta_unscaled)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:NAVic:NMESsage:NAV:IONospheric:BETA{channel_cmd_val}:UNSCaled {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:NAVic:[NMESsage]:[NAV]:IONospheric:BETA<CH>:UNSCaled \n
		Sets the parameters beta_0 to beta_3 of the satellite's navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beta')
			:return: beta_unscaled: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:NAVic:NMESsage:NAV:IONospheric:BETA{channel_cmd_val}:UNSCaled?')
		return Conversions.str_to_int(response)
