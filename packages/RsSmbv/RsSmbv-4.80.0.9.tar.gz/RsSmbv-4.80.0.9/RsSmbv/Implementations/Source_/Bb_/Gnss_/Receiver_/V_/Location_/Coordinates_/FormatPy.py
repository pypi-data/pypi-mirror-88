from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FormatPy:
	"""FormatPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("formatPy", core, parent)

	def set(self, position_format: enums.PositionFormat, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:COORdinates:FORMat \n
		Sets the format in which the latitude and longitude are set. \n
			:param position_format: DMS| DECimal
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(position_format, enums.PositionFormat)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:COORdinates:FORMat {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.PositionFormat:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:COORdinates:FORMat \n
		Sets the format in which the latitude and longitude are set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: position_format: DMS| DECimal"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:COORdinates:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.PositionFormat)
