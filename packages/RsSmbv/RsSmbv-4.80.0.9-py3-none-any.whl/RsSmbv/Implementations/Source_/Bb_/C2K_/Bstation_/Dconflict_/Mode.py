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

	def set(self, mode: enums.Cdma2KdomConfModeDn, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:DCONflict:MODE \n
		The command switches the order of the spreading codes. \n
			:param mode: HAD| BREV HAD the code channels are displayed in the order determined by the Hadamard matrix. The codes are numbered as Walsh codes according to the standard. BREV the code channels are displayed in the order defined by the Orthogonal Variable Spreading Factor (OVSF) code tree (3GPP code) .
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.enum_scalar_to_str(mode, enums.Cdma2KdomConfModeDn)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:DCONflict:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.Cdma2KdomConfModeDn:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:DCONflict:MODE \n
		The command switches the order of the spreading codes. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: mode: HAD| BREV HAD the code channels are displayed in the order determined by the Hadamard matrix. The codes are numbered as Walsh codes according to the standard. BREV the code channels are displayed in the order defined by the Orthogonal Variable Spreading Factor (OVSF) code tree (3GPP code) ."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:DCONflict:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KdomConfModeDn)
