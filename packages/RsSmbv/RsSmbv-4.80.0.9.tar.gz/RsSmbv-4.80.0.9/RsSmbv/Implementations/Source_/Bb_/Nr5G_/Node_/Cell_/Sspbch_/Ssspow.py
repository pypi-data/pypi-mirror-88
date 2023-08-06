from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssspow:
	"""Ssspow commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssspow", core, parent)

	def set(self, sss_power: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:SSSPow \n
		Sets the power of the SSS/PSS/PBCH allocations relative to the power of the other resource elements. \n
			:param sss_power: float Range: -80.0 to 10.0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')"""
		param = Conversions.decimal_value_to_str(sss_power)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:SSSPow {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:SSSPow \n
		Sets the power of the SSS/PSS/PBCH allocations relative to the power of the other resource elements. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:return: sss_power: float Range: -80.0 to 10.0"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:SSSPow?')
		return Conversions.str_to_float(response)
