from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Config:
	"""Config commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("config", core, parent)

	def set(self, predefined_confi: enums.DopplerConfig, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:SDYNamics:CONFig \n
		Selects between the predefined velocity profiles or a user-defined one. \n
			:param predefined_confi: USER| VEL1| VEL2 USER User-defined Profile parametrs are configurable. VEL1 Low dynamics Profile parametrs are read-only. VEL2 High dynamics Profile parametrs are read-only.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		param = Conversions.enum_scalar_to_str(predefined_confi, enums.DopplerConfig)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:SDYNamics:CONFig {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.DopplerConfig:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou<ST>:SDYNamics:CONFig \n
		Selects between the predefined velocity profiles or a user-defined one. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:return: predefined_confi: USER| VEL1| VEL2 USER User-defined Profile parametrs are configurable. VEL1 Low dynamics Profile parametrs are read-only. VEL2 High dynamics Profile parametrs are read-only."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:BEIDou{stream_cmd_val}:SDYNamics:CONFig?')
		return Conversions.str_to_scalar_enum(response, enums.DopplerConfig)
