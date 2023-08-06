from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.Cdma2KtxDivMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:TDIVersity:MODE \n
		The command selects the diversity scheme. Command method RsSmbv.Source.Bb.C2K.Bstation.Tdiversity.set activates transmit
		diversity and selects the antenna. \n
			:param mode: OTD| STS OTD Orthogonal Transmit Diversity Mode. STS Space Time Spreading Mode.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.enum_scalar_to_str(mode, enums.Cdma2KtxDivMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:TDIVersity:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.Cdma2KtxDivMode:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:TDIVersity:MODE \n
		The command selects the diversity scheme. Command method RsSmbv.Source.Bb.C2K.Bstation.Tdiversity.set activates transmit
		diversity and selects the antenna. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: mode: OTD| STS OTD Orthogonal Transmit Diversity Mode. STS Space Time Spreading Mode."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:TDIVersity:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KtxDivMode)
