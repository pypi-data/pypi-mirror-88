from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zp:
	"""Zp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zp", core, parent)

	def set(self, zero_power: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:CSIRs<ST>:ZP \n
		Sets the used CSI-RS configurations in the zero transmission power subframes. \n
			:param zero_power: integer In the user interface, the 16 bits are set as a hexadecimal value. In the remote control, as a decimal value. Range: 0 to 16 bit
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Csirs')"""
		param = Conversions.decimal_value_to_str(zero_power)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:CSIRs{stream_cmd_val}:ZP {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:CSIRs<ST>:ZP \n
		Sets the used CSI-RS configurations in the zero transmission power subframes. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Csirs')
			:return: zero_power: integer In the user interface, the 16 bits are set as a hexadecimal value. In the remote control, as a decimal value. Range: 0 to 16 bit"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:CSIRs{stream_cmd_val}:ZP?')
		return Conversions.str_to_int(response)
