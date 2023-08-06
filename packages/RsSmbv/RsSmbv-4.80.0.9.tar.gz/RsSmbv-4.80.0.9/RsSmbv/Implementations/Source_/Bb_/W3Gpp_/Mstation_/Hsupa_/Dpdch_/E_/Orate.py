from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Orate:
	"""Orate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("orate", core, parent)

	def set(self, orate: enums.WcdmaSymbRateEdPdchOverallSymbRate, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPDCh:E:ORATe \n
		Sets the overall symbol rate of all the E-DPDCH channels. \n
			:param orate: D15K| D30K| D60K| D120k| D240k| D480k| D960k| D1920k| D2X1920K| D2X960K2X1920K| D2880k| D3840k| D4800k| D5760k
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(orate, enums.WcdmaSymbRateEdPdchOverallSymbRate)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPDCh:E:ORATe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.WcdmaSymbRateEdPdchOverallSymbRate:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPDCh:E:ORATe \n
		Sets the overall symbol rate of all the E-DPDCH channels. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: orate: D15K| D30K| D60K| D120k| D240k| D480k| D960k| D1920k| D2X1920K| D2X960K2X1920K| D2880k| D3840k| D4800k| D5760k"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPDCh:E:ORATe?')
		return Conversions.str_to_scalar_enum(response, enums.WcdmaSymbRateEdPdchOverallSymbRate)
