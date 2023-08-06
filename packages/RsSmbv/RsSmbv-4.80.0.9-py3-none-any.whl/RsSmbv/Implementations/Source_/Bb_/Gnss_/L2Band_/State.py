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

	def set(self, l_2_band_state: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:L2Band<CH>:[STATe] \n
		Activates the RF band. \n
			:param l_2_band_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'L2Band')"""
		param = Conversions.bool_to_str(l_2_band_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:L2Band{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:GNSS:L2Band<CH>:[STATe] \n
		Activates the RF band. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'L2Band')
			:return: l_2_band_state: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:L2Band{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
