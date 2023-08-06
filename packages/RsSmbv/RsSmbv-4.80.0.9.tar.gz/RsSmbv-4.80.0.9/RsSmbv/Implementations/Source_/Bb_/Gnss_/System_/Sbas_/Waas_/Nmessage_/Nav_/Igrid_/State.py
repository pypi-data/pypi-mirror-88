from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SYSTem:SBAS:WAAS<ST>:NMESsage:NAV:IGRid:STATe \n
		Enables generation of the particular SBAS correction data. \n
			:param state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:WAAS{stream_cmd_val}:NMESsage:NAV:IGRid:STATe {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:GNSS:SYSTem:SBAS:WAAS<ST>:NMESsage:NAV:IGRid:STATe \n
		Enables generation of the particular SBAS correction data. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:WAAS{stream_cmd_val}:NMESsage:NAV:IGRid:STATe?')
		return Conversions.str_to_bool(response)
