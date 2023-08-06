from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.Utilities import trim_str_response
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	# noinspection PyTypeChecker
	class DpatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Dpattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Dpattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dpattern: List[str] = None
			self.Bit_Count: int = None

	def get_dpattern(self) -> DpatternStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DATA:DPATtern \n
		Specifies the user-defined pattern. The setting is relevant for method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.Data.valuePATTern \n
			:return: structure: for return value, see the help for DpatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DATA:DPATtern?', self.__class__.DpatternStruct())

	def set_dpattern(self, value: DpatternStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DATA:DPATtern \n
		Specifies the user-defined pattern. The setting is relevant for method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.Data.valuePATTern \n
			:param value: see the help for DpatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DATA:DPATtern', value)

	def get_dselection(self) -> str:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DATA:DSELection \n
		Specifies data list file. The setting is relevant for method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Data.
		valueDLISt \n
			:return: dselection: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DATA:DSELection?')
		return trim_str_response(response)

	def set_dselection(self, dselection: str) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DATA:DSELection \n
		Specifies data list file. The setting is relevant for method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Data.
		valueDLISt \n
			:param dselection: string
		"""
		param = Conversions.value_to_quoted_str(dselection)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DATA:DSELection {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.BtoDataSourc:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DATA \n
		Selects the pattern source used for the payload. \n
			:return: data: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt ALL0 / ALL1 All 0 or all 1 pattern PATTern User-defined pattern. The pattern can be specified via: method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Data.dpattern PNxx Pseudo-random bit sequences (PRBS) of a length of xx bits. The length in bit can be 9, 11, 15, 16, 20, 21, or 23. DLISt Internal data list is used. The data list can be specified via: method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Data.dselection
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.BtoDataSourc)

	def set_value(self, data: enums.BtoDataSourc) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DATA \n
		Selects the pattern source used for the payload. \n
			:param data: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt ALL0 / ALL1 All 0 or all 1 pattern PATTern User-defined pattern. The pattern can be specified via: method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Data.dpattern PNxx Pseudo-random bit sequences (PRBS) of a length of xx bits. The length in bit can be 9, 11, 15, 16, 20, 21, or 23. DLISt Internal data list is used. The data list can be specified via: method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Data.dselection
		"""
		param = Conversions.enum_scalar_to_str(data, enums.BtoDataSourc)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DATA {param}')
