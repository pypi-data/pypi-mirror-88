from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prach:
	"""Prach commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prach", core, parent)

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.TcwpRachFormat:
		"""[SOURce<HW>]:BB:NR5G:TCW:WS:PRACh:FORMat \n
		Sets the designated PRACH preamble format. The preamble is used to obtain the UL synchronization. In 5G NR, there are 64
		preambles defined in each time-frequency PRACH occasion. The preamble consists of two parts cyclic prefix (CP) and
		preamble sequence. In 5G NR, there are 13 types of preamble format supported known as format 0, format 1, format 2,
		format 3, format A1, format A2, format A3, format B1, format B2, format B3, format B4, format C0, format C1. \n
			:return: prach_format: F0| FA1| FA2| FA3| FB4| FC0| FC2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:PRACh:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.TcwpRachFormat)

	def set_format_py(self, prach_format: enums.TcwpRachFormat) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:WS:PRACh:FORMat \n
		Sets the designated PRACH preamble format. The preamble is used to obtain the UL synchronization. In 5G NR, there are 64
		preambles defined in each time-frequency PRACH occasion. The preamble consists of two parts cyclic prefix (CP) and
		preamble sequence. In 5G NR, there are 13 types of preamble format supported known as format 0, format 1, format 2,
		format 3, format A1, format A2, format A3, format B1, format B2, format B3, format B4, format C0, format C1. \n
			:param prach_format: F0| FA1| FA2| FA3| FB4| FC0| FC2
		"""
		param = Conversions.enum_scalar_to_str(prach_format, enums.TcwpRachFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:PRACh:FORMat {param}')

	# noinspection PyTypeChecker
	def get_sc_spacing(self) -> enums.TcwpRachNum:
		"""[SOURce<HW>]:BB:NR5G:TCW:WS:PRACh:SCSPacing \n
		Sets the subcarrier spacing using normal cyclic prefix (NCP) or extended cyclic prefix (ECP) . \n
			:return: prach_scs: N1_25| N15| N30| N60| N120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:PRACh:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.TcwpRachNum)

	def set_sc_spacing(self, prach_scs: enums.TcwpRachNum) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:WS:PRACh:SCSPacing \n
		Sets the subcarrier spacing using normal cyclic prefix (NCP) or extended cyclic prefix (ECP) . \n
			:param prach_scs: N1_25| N15| N30| N60| N120
		"""
		param = Conversions.enum_scalar_to_str(prach_scs, enums.TcwpRachNum)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:PRACh:SCSPacing {param}')
