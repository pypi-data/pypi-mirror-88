from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Yaw:
	"""Yaw commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("yaw", core, parent)

	def set(self, yaw: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ATTitude:YAW \n
		Sets the attitude parameters relative to the local horizon. \n
			:param yaw: float Range: -180 to 180
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.decimal_value_to_str(yaw)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ATTitude:YAW {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ATTitude:YAW \n
		Sets the attitude parameters relative to the local horizon. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: yaw: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ATTitude:YAW?')
		return Conversions.str_to_float(response)
