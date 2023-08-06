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
class Acad:
	"""Acad commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acad", core, parent)

	# noinspection PyTypeChecker
	class ApatternStruct(StructBase):
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

	def get_apattern(self) -> ApatternStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:APATtern \n
		Specifies user-defined pattern. The settings is relevant for method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.
		Acad.valuePATTern \n
			:return: structure: for return value, see the help for ApatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:APATtern?', self.__class__.ApatternStruct())

	def set_apattern(self, value: ApatternStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:APATtern \n
		Specifies user-defined pattern. The settings is relevant for method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.
		Acad.valuePATTern \n
			:param value: see the help for ApatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:APATtern', value)

	def get_aselection(self) -> str:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:ASELection \n
		Specifies data list file. The settings is relevant for method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Acad.
		valueDLISt \n
			:return: dselection: string Path and file name.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:ASELection?')
		return trim_str_response(response)

	def set_aselection(self, dselection: str) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:ASELection \n
		Specifies data list file. The settings is relevant for method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Acad.
		valueDLISt \n
			:param dselection: string Path and file name.
		"""
		param = Conversions.value_to_quoted_str(dselection)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD:ASELection {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.BtoDataSourc:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD \n
		Specifies the pattern source used for additional controller advertising data (ACAD) . \n
			:return: data: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt ALL0 / ALL1 All 0 or all 1 pattern PATTern User-defined pattern. The pattern can be specified via: method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Acad.apattern PNxx Pseudo-random bit sequences (PRBS) of a length of xx bits. The length in bit can be 9, 11, 15, 16, 20, 21, or 23. DLISt Internal ACAD data list is used. The data list can be specified via: method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Acad.aselection
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD?')
		return Conversions.str_to_scalar_enum(response, enums.BtoDataSourc)

	def set_value(self, data: enums.BtoDataSourc) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD \n
		Specifies the pattern source used for additional controller advertising data (ACAD) . \n
			:param data: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt ALL0 / ALL1 All 0 or all 1 pattern PATTern User-defined pattern. The pattern can be specified via: method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Acad.apattern PNxx Pseudo-random bit sequences (PRBS) of a length of xx bits. The length in bit can be 9, 11, 15, 16, 20, 21, or 23. DLISt Internal ACAD data list is used. The data list can be specified via: method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.Acad.aselection
		"""
		param = Conversions.enum_scalar_to_str(data, enums.BtoDataSourc)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACAD {param}')
