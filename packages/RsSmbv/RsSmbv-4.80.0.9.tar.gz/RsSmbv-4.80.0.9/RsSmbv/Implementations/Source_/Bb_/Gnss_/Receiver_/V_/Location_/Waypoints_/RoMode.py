from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RoMode:
	"""RoMode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("roMode", core, parent)

	def set(self, ro_mode: enums.ReadOutMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:WAYPoints:ROMode \n
		Defines the way the waypoint/attitude file is processed. \n
			:param ro_mode: CYCLic| RTRip| OWAY
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(ro_mode, enums.ReadOutMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:WAYPoints:ROMode {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.ReadOutMode:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:WAYPoints:ROMode \n
		Defines the way the waypoint/attitude file is processed. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: ro_mode: CYCLic| RTRip| OWAY"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:WAYPoints:ROMode?')
		return Conversions.str_to_scalar_enum(response, enums.ReadOutMode)
