from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rconfiguration:
	"""Rconfiguration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rconfiguration", core, parent)

	def set(self, rconfiguration: enums.Cdma2KradioConf, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:RCONfiguration \n
		Selects the radio configuration for the traffic channel. The settings of the channel table parameters are specific for
		the selected radio configuration. \n
			:param rconfiguration: 1| 2| 3| 4| 5
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')"""
		param = Conversions.enum_scalar_to_str(rconfiguration, enums.Cdma2KradioConf)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:RCONfiguration {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default) -> enums.Cdma2KradioConf:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:RCONfiguration \n
		Selects the radio configuration for the traffic channel. The settings of the channel table parameters are specific for
		the selected radio configuration. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:return: rconfiguration: 1| 2| 3| 4| 5"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:RCONfiguration?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KradioConf)
