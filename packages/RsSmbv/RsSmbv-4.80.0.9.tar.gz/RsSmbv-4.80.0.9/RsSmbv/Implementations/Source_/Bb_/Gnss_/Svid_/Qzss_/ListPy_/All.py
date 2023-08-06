from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def get(self, stream=repcap.Stream.Default) -> List[int]:
		"""[SOURce<HW>]:BB:GNSS:SVID:QZSS<ST>:LIST:ALL \n
		Queries the SV IDs of all satellites of the GNSS system. The query lists SV IDs of the satellites included in and
		excluded from the satellite constellation (Figure 'Satellites constellation: Understanding the displayed information') . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:return: id_pi_db_gnss_sat_sv_id_list_all: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_bin_or_ascii_int_list(f'SOURce<HwInstance>:BB:GNSS:SVID:QZSS{stream_cmd_val}:LIST:ALL?')
		return response
