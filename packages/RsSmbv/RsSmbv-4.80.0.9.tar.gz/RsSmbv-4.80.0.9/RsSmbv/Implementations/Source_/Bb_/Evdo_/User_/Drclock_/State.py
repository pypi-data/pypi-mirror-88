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

	def set(self, state: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:DRCLock:STATe \n
		Sets the state of the DRC (Data Rate Control) Lock bit for the selected user. Note: Changes in the DRC Lock state are
		only considered at the interval defined by the parameter DRC Lock Length. \n
			:param state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:DRCLock:STATe {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:DRCLock:STATe \n
		Sets the state of the DRC (Data Rate Control) Lock bit for the selected user. Note: Changes in the DRC Lock state are
		only considered at the interval defined by the parameter DRC Lock Length. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:DRCLock:STATe?')
		return Conversions.str_to_bool(response)
