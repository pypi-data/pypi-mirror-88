from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BmpLength:
	"""BmpLength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bmpLength", core, parent)

	def set(self, bmp_length: enums.EutraSlV2XbMpLength, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:BMPLength \n
		Sets the bitmap length. To set the subframe bitmap, use the commands method RsSmbv.Source.Bb.Eutra.Ul.Ue.Sl.V2X.BitLow.
		set and method RsSmbv.Source.Bb.Eutra.Ul.Ue.Sl.V2X.BitHigh.set. \n
			:param bmp_length: 10| 16| 20| 30| 40| 50| 60| 100
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(bmp_length, enums.EutraSlV2XbMpLength)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:BMPLength {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraSlV2XbMpLength:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:BMPLength \n
		Sets the bitmap length. To set the subframe bitmap, use the commands method RsSmbv.Source.Bb.Eutra.Ul.Ue.Sl.V2X.BitLow.
		set and method RsSmbv.Source.Bb.Eutra.Ul.Ue.Sl.V2X.BitHigh.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: bmp_length: 10| 16| 20| 30| 40| 50| 60| 100"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:BMPLength?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSlV2XbMpLength)
