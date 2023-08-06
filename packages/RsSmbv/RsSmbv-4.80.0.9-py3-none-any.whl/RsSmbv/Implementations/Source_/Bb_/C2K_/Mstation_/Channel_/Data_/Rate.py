from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rate:
	"""Rate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rate", core, parent)

	def set(self, rate: enums.Cdma2KdataRate, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation<ST>:CHANnel<CH>:DATA:RATE \n
		The command sets the data rate for the specified channel. The value range depends on the channel type, the selected radio
		configuration and the frame length. For the traffic channels, this value is specific for the selected radio configuration.
		The value range of the data rate depends on the channel type and the frame length. If the frame length is changed so that
		the set data rate becomes invalid, the next permissible value is automatically set. \n
			:param rate: DR1K2| DR1K3| DR1K5| DR1K8| DR2K4| DR2K7| DR3K6| DR4K8| DR7K2| DR9K6| DR14K4| DR19K2| DR28K8| DR38K4| DR57K6| DR76K8| DR115K2| DR153K6| DR230K4| DR259K2| DR307K2| DR460K8| DR518K4| DR614K4| DR1036K8| NUSed
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(rate, enums.Cdma2KdataRate)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:DATA:RATE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.Cdma2KdataRate:
		"""[SOURce<HW>]:BB:C2K:MSTation<ST>:CHANnel<CH>:DATA:RATE \n
		The command sets the data rate for the specified channel. The value range depends on the channel type, the selected radio
		configuration and the frame length. For the traffic channels, this value is specific for the selected radio configuration.
		The value range of the data rate depends on the channel type and the frame length. If the frame length is changed so that
		the set data rate becomes invalid, the next permissible value is automatically set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: rate: DR1K2| DR1K3| DR1K5| DR1K8| DR2K4| DR2K7| DR3K6| DR4K8| DR7K2| DR9K6| DR14K4| DR19K2| DR28K8| DR38K4| DR57K6| DR76K8| DR115K2| DR153K6| DR230K4| DR259K2| DR307K2| DR460K8| DR518K4| DR614K4| DR1036K8| NUSed"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:DATA:RATE?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KdataRate)
