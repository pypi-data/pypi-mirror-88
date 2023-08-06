from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sformat:
	"""Sformat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sformat", core, parent)

	def set(self, sf_ormat: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:SFORmat \n
		The command sets the slot format of the selected channel. The value range depends on the selected channel.
		The slot format determines the symbol rate (and thus the range of values for the channelization code) , the TFCI state
		and the pilot length. If the value of any one of the four parameters is changed, all the other parameters are adapted as
		necessary. In the case of enhanced channels with active channel coding, the selected channel coding also affects the slot
		format and thus the remaining parameters. If these parameters are changed, the channel coding type is set to user. \n
			:param sf_ormat: integer Range: 0 to dynamic
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(sf_ormat)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:SFORmat {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:SFORmat \n
		The command sets the slot format of the selected channel. The value range depends on the selected channel.
		The slot format determines the symbol rate (and thus the range of values for the channelization code) , the TFCI state
		and the pilot length. If the value of any one of the four parameters is changed, all the other parameters are adapted as
		necessary. In the case of enhanced channels with active channel coding, the selected channel coding also affects the slot
		format and thus the remaining parameters. If these parameters are changed, the channel coding type is set to user. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: sf_ormat: integer Range: 0 to dynamic"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:SFORmat?')
		return Conversions.str_to_int(response)
