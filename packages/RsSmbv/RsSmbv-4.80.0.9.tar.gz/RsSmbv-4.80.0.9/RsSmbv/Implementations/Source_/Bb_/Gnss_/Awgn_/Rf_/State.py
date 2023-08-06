from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, awgn_state: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:STATe \n
		Activates/deactivates the generation of an AWGN signal. The interferer (AWGN or CW interferer, depending on the selected
		mode) is generated after the generator is activated. \n
			:param awgn_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.bool_to_str(awgn_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:STATe \n
		Activates/deactivates the generation of an AWGN signal. The interferer (AWGN or CW interferer, depending on the selected
		mode) is generated after the generator is activated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: awgn_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
