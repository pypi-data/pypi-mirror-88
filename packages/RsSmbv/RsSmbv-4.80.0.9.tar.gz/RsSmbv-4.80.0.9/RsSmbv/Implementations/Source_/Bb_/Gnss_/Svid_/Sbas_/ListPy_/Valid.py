from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Valid:
	"""Valid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("valid", core, parent)

	def get(self, stream=repcap.Stream.Default) -> List[int]:
		"""[SOURce<HW>]:BB:GNSS:SVID:SBAS<ST>:LIST:[VALid] \n
		Queries the SV IDs of all valid satellites for the GNSS system. The query lists SV IDs of the satellites included in the
		satellite constellation. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: gnss_sat_sv_id_list: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_bin_or_ascii_int_list(f'SOURce<HwInstance>:BB:GNSS:SVID:SBAS{stream_cmd_val}:LIST:VALid?')
		return response
