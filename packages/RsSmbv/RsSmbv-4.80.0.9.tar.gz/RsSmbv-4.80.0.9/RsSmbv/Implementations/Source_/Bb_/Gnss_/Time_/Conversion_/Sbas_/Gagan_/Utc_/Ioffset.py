from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ioffset:
	"""Ioffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ioffset", core, parent)

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:SBAS<ST>:GAGAN:UTC:IOFFset \n
		Queries the integer offset. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: integer_offset: integer Range: 0 to 604800"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:SBAS{stream_cmd_val}:GAGAN:UTC:IOFFset?')
		return Conversions.str_to_int(response)
