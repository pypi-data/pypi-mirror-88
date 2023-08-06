from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccode:
	"""Ccode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccode", core, parent)

	def set(self, ccode: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:CCODe \n
		The command sets the channelization code (formerly the spreading code number) . The range of values of the channelization
		code depends on the symbol rate of the channel. The standard assigns a fixed channelization code to some channels
		(P-CPICH, for example, always uses channelization code 0) . [chip-rate(=3.84Mcps) / symbol_rate] - 1 The slot format
		determines the symbol rate (and thus the range of values for the channelization code) , the TFCI state and the pilot
		length. If the value of any one of the four parameters is changed, all the other parameters are adapted as necessary. In
		the case of enhanced channels with active channel coding, the selected channel coding also affects the slot format and
		thus the remaining parameters. If these parameters are changed, the channel coding type is set to user. \n
			:param ccode: integer Range: 0 to 511
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(ccode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:CCODe {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:CCODe \n
		The command sets the channelization code (formerly the spreading code number) . The range of values of the channelization
		code depends on the symbol rate of the channel. The standard assigns a fixed channelization code to some channels
		(P-CPICH, for example, always uses channelization code 0) . [chip-rate(=3.84Mcps) / symbol_rate] - 1 The slot format
		determines the symbol rate (and thus the range of values for the channelization code) , the TFCI state and the pilot
		length. If the value of any one of the four parameters is changed, all the other parameters are adapted as necessary. In
		the case of enhanced channels with active channel coding, the selected channel coding also affects the slot format and
		thus the remaining parameters. If these parameters are changed, the channel coding type is set to user. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: ccode: integer Range: 0 to 511"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:CCODe?')
		return Conversions.str_to_int(response)
