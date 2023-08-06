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
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:DATA:DPATtern \n
		Sets the data pattern, if the data source PATT is selected. \n
			:return: structure: for return value, see the help for DpatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:LORA:FCONfiguration:DATA:DPATtern?', self.__class__.DpatternStruct())

	def set_dpattern(self, value: DpatternStruct) -> None:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:DATA:DPATtern \n
		Sets the data pattern, if the data source PATT is selected. \n
			:param value: see the help for DpatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:LORA:FCONfiguration:DATA:DPATtern', value)

	def get_dselection(self) -> str:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:DATA:DSELection \n
		Selects an existing data list file from the default directory or from the specific directory. The data list is only used,
		if the data source DLIS is selected. \n
			:return: dselection: string Filename incl. file extension or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:DATA:DSELection?')
		return trim_str_response(response)

	def set_dselection(self, dselection: str) -> None:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:DATA:DSELection \n
		Selects an existing data list file from the default directory or from the specific directory. The data list is only used,
		if the data source DLIS is selected. \n
			:param dselection: string Filename incl. file extension or complete file path
		"""
		param = Conversions.value_to_quoted_str(dselection)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:DATA:DSELection {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.DataSour:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:DATA \n
		Sets the data source for the payload data in a LoRa frame. \n
			:return: data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt PNxx The pseudo-random sequence generator is used as the data source. There is a choice of different lengths of random sequence. DLISt A data list is used. The data list is selected with the aid of command SOURce:BB:LORA:DATA DLISt. ALL0 | ALL1 Internal 0 or 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined with the aid of command :SOURce:BB:LORA:DATA PATTern.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSour)

	def set_value(self, data: enums.DataSour) -> None:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:DATA \n
		Sets the data source for the payload data in a LoRa frame. \n
			:param data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt PNxx The pseudo-random sequence generator is used as the data source. There is a choice of different lengths of random sequence. DLISt A data list is used. The data list is selected with the aid of command SOURce:BB:LORA:DATA DLISt. ALL0 | ALL1 Internal 0 or 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined with the aid of command :SOURce:BB:LORA:DATA PATTern.
		"""
		param = Conversions.enum_scalar_to_str(data, enums.DataSour)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:DATA {param}')
