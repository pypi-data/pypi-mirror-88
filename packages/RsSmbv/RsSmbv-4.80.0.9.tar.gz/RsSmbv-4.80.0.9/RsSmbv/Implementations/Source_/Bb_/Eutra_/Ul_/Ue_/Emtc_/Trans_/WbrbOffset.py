from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WbrbOffset:
	"""WbrbOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wbrbOffset", core, parent)

	def set(self, wide_band_rb_offs: enums.EutraEmtcVrbOffs, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:TRANs<CH>:WBRBoffset \n
		Shifts the selected number of resource blocks within the wideband. \n
			:param wide_band_rb_offs: OS0| OS3| OS6| OS9| OS12| OS15| OS18| OS21
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')"""
		param = Conversions.enum_scalar_to_str(wide_band_rb_offs, enums.EutraEmtcVrbOffs)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:EMTC:TRANs{channel_cmd_val}:WBRBoffset {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraEmtcVrbOffs:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:TRANs<CH>:WBRBoffset \n
		Shifts the selected number of resource blocks within the wideband. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: wide_band_rb_offs: OS0| OS3| OS6| OS9| OS12| OS15| OS18| OS21"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:EMTC:TRANs{channel_cmd_val}:WBRBoffset?')
		return Conversions.str_to_scalar_enum(response, enums.EutraEmtcVrbOffs)
