from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:GNSS:SYSTem:SBAS<ST>:[STATe] \n
		Queries if at least one of the SBAS system is enabled. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: state: 0| 1| OFF| ON 1 At least one SBAS system is enabled. To enable each of the SBAS systems, use the corresponding command, e.g. method RsSmbv.Source.Bb.Gnss.System.Sbas.State.get_. 0 All SBAS systems are disabled."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS{stream_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
