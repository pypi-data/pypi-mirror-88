from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Flength:
	"""Flength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("flength", core, parent)

	def set(self, flength: enums.Cdma2KframLenUp, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation<ST>:CHANnel<CH>:FLENgth \n
		The command sets the frame length of the selected channel. The value range depends on the channel type and the selected
		radio configuration For the traffic channels, this value is specific for the selected radio configuration. The frame
		length affects the data rates that are possible within a channel. Changing the frame length may lead to a change of data
		rate. \n
			:param flength: 5| 10| 20| 26.6| 40| 80
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(flength, enums.Cdma2KframLenUp)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:FLENgth {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.Cdma2KframLenUp:
		"""[SOURce<HW>]:BB:C2K:MSTation<ST>:CHANnel<CH>:FLENgth \n
		The command sets the frame length of the selected channel. The value range depends on the channel type and the selected
		radio configuration For the traffic channels, this value is specific for the selected radio configuration. The frame
		length affects the data rates that are possible within a channel. Changing the frame length may lead to a change of data
		rate. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: flength: 5| 10| 20| 26.6| 40| 80"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:FLENgth?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KframLenUp)
