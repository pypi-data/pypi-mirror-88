from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sscg:
	"""Sscg commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sscg", core, parent)

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:SSCG \n
		The command queries the secondary synchronization code group. This parameter is specified in the table defined by the
		3GPP standard 'Allocation of SSCs for secondary SCH'. This table assigns a specific spreading code to the synchronization
		code symbol for every slot in the frame. The value is calculated from the scrambling code. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: sscg: integer Range: 0 to 63"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:SSCG?')
		return Conversions.str_to_int(response)
