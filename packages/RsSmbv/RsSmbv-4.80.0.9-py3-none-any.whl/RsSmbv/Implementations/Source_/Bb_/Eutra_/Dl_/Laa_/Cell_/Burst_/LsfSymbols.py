from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LsfSymbols:
	"""LsfSymbols commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lsfSymbols", core, parent)

	def set(self, last_sf_symb: enums.EutraLaalAstSf, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:LSFSymbols \n
		Sets the number of OFDM symbols in the last subframe of the LAA burst. \n
			:param last_sf_symb: SY3| SY6| SY9| SY10| SY11| SY12| SY14
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')"""
		param = Conversions.enum_scalar_to_str(last_sf_symb, enums.EutraLaalAstSf)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:LSFSymbols {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.EutraLaalAstSf:
		"""[SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:LSFSymbols \n
		Sets the number of OFDM symbols in the last subframe of the LAA burst. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')
			:return: last_sf_symb: SY3| SY6| SY9| SY10| SY11| SY12| SY14"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:LSFSymbols?')
		return Conversions.str_to_scalar_enum(response, enums.EutraLaalAstSf)
