from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scheme:
	"""Scheme commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scheme", core, parent)

	def set(self, scheme: enums.EutraDlecpRecScheme, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PRECoding:SCHeme \n
		Selects the precoding scheme for PDCCH. \n
			:param scheme: NONE| TXD NONE Disables precoding. TXD Precoding for transmit diversity will be performed according to 3GPP TS 36.211 and the selected parameters
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(scheme, enums.EutraDlecpRecScheme)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PRECoding:SCHeme {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraDlecpRecScheme:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PRECoding:SCHeme \n
		Selects the precoding scheme for PDCCH. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: scheme: NONE| TXD NONE Disables precoding. TXD Precoding for transmit diversity will be performed according to 3GPP TS 36.211 and the selected parameters"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PRECoding:SCHeme?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDlecpRecScheme)
