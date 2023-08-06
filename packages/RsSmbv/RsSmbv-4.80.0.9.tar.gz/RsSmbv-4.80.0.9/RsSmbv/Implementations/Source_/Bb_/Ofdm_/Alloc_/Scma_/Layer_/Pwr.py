from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pwr:
	"""Pwr commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pwr", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:SCMA:LAYer<ST>:PWR \n
		Applies a power offset to the selected layer relative to the others. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layer')
			:return: power: float Range: -80 to 10"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:SCMA:LAYer{stream_cmd_val}:PWR?')
		return Conversions.str_to_float(response)
