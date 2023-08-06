from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> enums.Cdma2KchanTypeDn:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:TYPE \n
		Queries the channel type. The channel type is firmly fixed for channel numbers 0-1 to 0-14 (CGR0:COFF1 to CGR0:COFF14) ,
		i.e. for the special channels (control and packet channels) . The remaining channel numbers are assigned to the
		individual code channels of the eight possible traffic channels. In this case, the first traffic channel occupies the
		range 1-1 to 1-8 (CGR1:COFF1 to CGR1:COFF8) , the second occupies the range 2-1 to 2-8 (CGR2:COFF1 to CGR2:COFF8) , etc.
		Since the type and number of code channels depends on the radio configuration of the channel, the channels x-2 to x-8 are
		variously occupied. X-1 is always the fundamental channel (F-FCH) of the traffic channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: type_py: F-PICH| F-SYNC| F-PCH| F-TDPICH| F-APICH| F-ATDPICH| F-BCH| F-QPCH| F-CPCCH| F-CACH| F-CCCH| F-DCCH| F-FCH| F-SCH| F-PDCCH| F-PDCH"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KchanTypeDn)
