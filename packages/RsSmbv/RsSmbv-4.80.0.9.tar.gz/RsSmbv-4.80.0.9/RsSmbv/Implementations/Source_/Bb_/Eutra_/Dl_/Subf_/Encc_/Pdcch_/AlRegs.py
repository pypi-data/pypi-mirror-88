from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlRegs:
	"""AlRegs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alRegs", core, parent)

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:ALRegs \n
		Defines the number of REGs that are actually allocated for PDCCH transmission (#REGs allocatedPDCCH) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: alloc_region_coun: integer Range: 0 to 1E5"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:ALRegs?')
		return Conversions.str_to_int(response)
