from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.Utilities import trim_str_response
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

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
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:DPATtern \n
		Selects the data for a pattern. \n
			:return: structure: for return value, see the help for DpatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:DPATtern?', self.__class__.DpatternStruct())

	def set_dpattern(self, value: DpatternStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:DPATtern \n
		Selects the data for a pattern. \n
			:param value: see the help for DpatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:DPATtern', value)

	def get_dselection(self) -> str:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:DSELection \n
		The command selects data list file. \n
			:return: dselection: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:DSELection?')
		return trim_str_response(response)

	def set_dselection(self, dselection: str) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:DSELection \n
		The command selects data list file. \n
			:param dselection: string
		"""
		param = Conversions.value_to_quoted_str(dselection)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:DSELection {param}')

	# noinspection PyTypeChecker
	class VdPatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Vd_Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Vd_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Vd_Pattern: List[str] = None
			self.Bit_Count: int = None

	def get_vd_pattern(self) -> VdPatternStruct:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:VDPAttern \n
		Sets the bit pattern for the voice data. \n
			:return: structure: for return value, see the help for VdPatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:VDPAttern?', self.__class__.VdPatternStruct())

	def set_vd_pattern(self, value: VdPatternStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:VDPAttern \n
		Sets the bit pattern for the voice data. \n
			:param value: see the help for VdPatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:VDPAttern', value)

	def get_vd_selection(self) -> str:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:VDSElection \n
		Selects the data list for voice data. \n
			:return: vd_selection: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:VDSElection?')
		return trim_str_response(response)

	def set_vd_selection(self, vd_selection: str) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA:VDSElection \n
		Selects the data list for voice data. \n
			:param vd_selection: string
		"""
		param = Conversions.value_to_quoted_str(vd_selection)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA:VDSElection {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.BtoDataSourc:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA \n
		Selects the data source used for the payload. \n
			:return: data: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.BtoDataSourc)

	def set_value(self, data: enums.BtoDataSourc) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DATA \n
		Selects the data source used for the payload. \n
			:param data: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt
		"""
		param = Conversions.enum_scalar_to_str(data, enums.BtoDataSourc)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DATA {param}')
