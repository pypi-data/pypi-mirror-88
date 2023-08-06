from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def set(self, srate: enums.SymbRate, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:SRATe \n
		The command sets the symbol rate of the selected channel. The value range depends on the selected channel and the
		selected slot format. The slot format determines the symbol rate (and thus the range of values for the channelization
		code) , the TFCI state and the pilot length. If the value of any one of the four parameters is changed, all the other
		parameters are adapted as necessary. In the case of enhanced channels with active channel coding, the selected channel
		coding also affects the slot format and thus the remaining parameters. If these parameters are changed, the channel
		coding type is set to user. \n
			:param srate: D7K5| D15K| D30K| D60K| D120k| D240k| D480k| D960k
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(srate, enums.SymbRate)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:SRATe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.SymbRate:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:SRATe \n
		The command sets the symbol rate of the selected channel. The value range depends on the selected channel and the
		selected slot format. The slot format determines the symbol rate (and thus the range of values for the channelization
		code) , the TFCI state and the pilot length. If the value of any one of the four parameters is changed, all the other
		parameters are adapted as necessary. In the case of enhanced channels with active channel coding, the selected channel
		coding also affects the slot format and thus the remaining parameters. If these parameters are changed, the channel
		coding type is set to user. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: srate: D7K5| D15K| D30K| D60K| D120k| D240k| D480k| D960k"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:SRATe?')
		return Conversions.str_to_scalar_enum(response, enums.SymbRate)
