from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PHYS:LCOD<CH>:STATe \n
		Specifies the physical layers for which the slave has a minimum number of used channels requirement. Information is
		signaled via LL_MIN_USED_CHANNELS_IND. You can enable one or more PHYs: L1M for LE uncoded 1 Msymbol/s PHY, L2M for LE
		uncoded 2 Msymbol/s PHY, and LCOD for LE coded 1 Msymbol/s PHY. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Lcod')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PHYS:LCOD{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PHYS:LCOD<CH>:STATe \n
		Specifies the physical layers for which the slave has a minimum number of used channels requirement. Information is
		signaled via LL_MIN_USED_CHANNELS_IND. You can enable one or more PHYs: L1M for LE uncoded 1 Msymbol/s PHY, L2M for LE
		uncoded 2 Msymbol/s PHY, and LCOD for LE coded 1 Msymbol/s PHY. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Lcod')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PHYS:LCOD{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
