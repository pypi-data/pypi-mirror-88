from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.TdscdmaDchCoding, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:TYPE \n
		The command sets the channel coding type. \n
			:param type_py: RMC12K2| RMC64K| RMC144K| RMC384K| RMC2048K| HRMC526K| HRMC730K| UP_RMC12K2| UP_RMC64K| UP_RMC144K| UP_RMC384K| HSDPA| HSUPA| HS_SICH| PLCCH| USER| USER
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.TdscdmaDchCoding)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TdscdmaDchCoding:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:TYPE \n
		The command sets the channel coding type. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: type_py: RMC12K2| RMC64K| RMC144K| RMC384K| RMC2048K| HRMC526K| HRMC730K| UP_RMC12K2| UP_RMC64K| UP_RMC144K| UP_RMC384K| HSDPA| HSUPA| HS_SICH| PLCCH| USER| USER"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaDchCoding)
