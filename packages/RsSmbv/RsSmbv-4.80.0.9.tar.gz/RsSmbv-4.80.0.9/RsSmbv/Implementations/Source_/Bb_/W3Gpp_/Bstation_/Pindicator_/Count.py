from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Count:
	"""Count commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("count", core, parent)

	def set(self, count: enums.PageInd, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:PINDicator:COUNt \n
		The command sets the number of page indicators (PI) per frame in the page indicator channel (PICH) . \n
			:param count: D18| D36| D72| D144
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.enum_scalar_to_str(count, enums.PageInd)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:PINDicator:COUNt {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.PageInd:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:PINDicator:COUNt \n
		The command sets the number of page indicators (PI) per frame in the page indicator channel (PICH) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: count: D18| D36| D72| D144"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:PINDicator:COUNt?')
		return Conversions.str_to_scalar_enum(response, enums.PageInd)
