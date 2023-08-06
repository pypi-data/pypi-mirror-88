from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offset", core, parent)

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:NAVic<ST>:OFFSet \n
		Queries the time offset between the time in the navigation standard and UTC. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: utc_offset: float Range: -1E6 to 1E6"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:NAVic{stream_cmd_val}:OFFSet?')
		return Conversions.str_to_float(response)
