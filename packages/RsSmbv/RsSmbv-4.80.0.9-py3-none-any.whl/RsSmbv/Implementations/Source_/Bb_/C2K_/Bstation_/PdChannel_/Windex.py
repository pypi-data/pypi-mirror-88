from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Windex:
	"""Windex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("windex", core, parent)

	def set(self, wi_ndex: enums.NumbersG, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:WINDex \n
		The command selects a standard Walsh set for F-PDCH. Four different sets are defined in the standard. \n
			:param wi_ndex: 0| 1| 2| 3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.enum_scalar_to_str(wi_ndex, enums.NumbersG)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:WINDex {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.NumbersG:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:WINDex \n
		The command selects a standard Walsh set for F-PDCH. Four different sets are defined in the standard. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: wi_ndex: 0| 1| 2| 3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:WINDex?')
		return Conversions.str_to_scalar_enum(response, enums.NumbersG)
