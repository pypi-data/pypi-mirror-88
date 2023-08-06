from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NzConfig:
	"""NzConfig commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nzConfig", core, parent)

	def set(self, non_zero_pwr_conf: enums.NumbersE, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:CSIRs<ST>:NZConfig \n
		Sets the CSI-RS configuration. \n
			:param non_zero_pwr_conf: 0| 1| 2| 3| 4| 5| 6| 7| 8| 9| 10| 11| 12| 13| 14| 15| 16| 17| 18| 19| 20| 21| 22| 23| 24| 25| 26| 27| 28| 29| 30| 31 Values outside the permitted discrete values are rounded down.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Csirs')"""
		param = Conversions.enum_scalar_to_str(non_zero_pwr_conf, enums.NumbersE)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:CSIRs{stream_cmd_val}:NZConfig {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.NumbersE:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:CSIRs<ST>:NZConfig \n
		Sets the CSI-RS configuration. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Csirs')
			:return: non_zero_pwr_conf: 0| 1| 2| 3| 4| 5| 6| 7| 8| 9| 10| 11| 12| 13| 14| 15| 16| 17| 18| 19| 20| 21| 22| 23| 24| 25| 26| 27| 28| 29| 30| 31 Values outside the permitted discrete values are rounded down."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:CSIRs{stream_cmd_val}:NZConfig?')
		return Conversions.str_to_scalar_enum(response, enums.NumbersE)
