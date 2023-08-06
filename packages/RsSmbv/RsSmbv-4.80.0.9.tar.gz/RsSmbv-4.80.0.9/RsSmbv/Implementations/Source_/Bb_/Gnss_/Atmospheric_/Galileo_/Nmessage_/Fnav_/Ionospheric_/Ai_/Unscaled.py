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

	def set(self, ai_unscaled: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:GALileo:[NMESsage]:[FNAV]:IONospheric:AI<CH>:UNSCaled \n
		Sets the parameters effective ionization level 1st to 3rd order of the satellite's navigation message. \n
			:param ai_unscaled: integer Range: a_i0 (0 to 2047) , a_i1 (-1024 to 1023) , a_i2 (-8192 to 8191)
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.decimal_value_to_str(ai_unscaled)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GALileo:NMESsage:FNAV:IONospheric:AI{channel_cmd_val}:UNSCaled {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:GALileo:[NMESsage]:[FNAV]:IONospheric:AI<CH>:UNSCaled \n
		Sets the parameters effective ionization level 1st to 3rd order of the satellite's navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: ai_unscaled: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GALileo:NMESsage:FNAV:IONospheric:AI{channel_cmd_val}:UNSCaled?')
		return Conversions.str_to_float(response)
