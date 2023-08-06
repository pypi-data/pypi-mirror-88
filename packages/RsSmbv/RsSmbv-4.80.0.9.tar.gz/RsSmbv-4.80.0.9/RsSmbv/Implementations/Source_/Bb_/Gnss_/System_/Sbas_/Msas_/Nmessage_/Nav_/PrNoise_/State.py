from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SYSTem:SBAS:MSAS<ST>:NMESsage:NAV:PRN<CH>:STATe \n
		Enables an SV ID/ SV PRN. \n
			:param state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'PrNoise')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:MSAS{stream_cmd_val}:NMESsage:NAV:PRN{channel_cmd_val}:STATe {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:GNSS:SYSTem:SBAS:MSAS<ST>:NMESsage:NAV:PRN<CH>:STATe \n
		Enables an SV ID/ SV PRN. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'PrNoise')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:MSAS{stream_cmd_val}:NMESsage:NAV:PRN{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
