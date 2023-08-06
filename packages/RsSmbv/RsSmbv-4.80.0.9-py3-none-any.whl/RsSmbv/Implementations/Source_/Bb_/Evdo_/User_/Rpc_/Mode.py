from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.EvdoRpcMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RPC:MODE \n
		Sets the operation mode for the Reverse Power Control (RPC) Channel within the MAC channel for the selected user. \n
			:param mode: HOLD| UP| DOWN| RANGe| PATTern
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(mode, enums.EvdoRpcMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RPC:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EvdoRpcMode:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RPC:MODE \n
		Sets the operation mode for the Reverse Power Control (RPC) Channel within the MAC channel for the selected user. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: mode: HOLD| UP| DOWN| RANGe| PATTern"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RPC:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoRpcMode)
