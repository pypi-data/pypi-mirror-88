from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FormatPy:
	"""FormatPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("formatPy", core, parent)

	def set(self, format_py: enums.EutraPdccFmt2, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:FORMat \n
		Sets the PDCCH format. \n
			:param format_py: VAR| -1| 0| 1| 2| 3 VAR Enables full flexibility by the configuration of the downlink control information (DCI) format and content. -1 Proprietary format for legacy support. 0 | 1 | 2 | 3 One PDCCH is transmitted on one, two, four or eight CCEs
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(format_py, enums.EutraPdccFmt2)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:FORMat {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraPdccFmt2:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:FORMat \n
		Sets the PDCCH format. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: format_py: VAR| -1| 0| 1| 2| 3 VAR Enables full flexibility by the configuration of the downlink control information (DCI) format and content. -1 Proprietary format for legacy support. 0 | 1 | 2 | 3 One PDCCH is transmitted on one, two, four or eight CCEs"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPdccFmt2)
