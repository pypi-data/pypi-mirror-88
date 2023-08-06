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
class Dumd:
	"""Dumd commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dumd", core, parent)

	# noinspection PyTypeChecker
	def get_data(self) -> enums.DataSour:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:DATA \n
		Selects the data source for dummy data. \n
			:return: data: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:DUMD:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSour)

	def set_data(self, data: enums.DataSour) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:DATA \n
		Selects the data source for dummy data. \n
			:param data: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE
		"""
		param = Conversions.enum_scalar_to_str(data, enums.DataSour)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DUMD:DATA {param}')

	def get_dselect(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:DSELect \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:return: filename: string Filename incl. file extension or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:DUMD:DSELect?')
		return trim_str_response(response)

	def set_dselect(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:DSELect \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param filename: string Filename incl. file extension or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DUMD:DSELect {param}')

	# noinspection PyTypeChecker
	def get_modulation(self) -> enums.ModulationD:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:MODulation \n
		Selects modulation for dummy data. \n
			:return: modulation: QPSK| QAM16| QAM64 | QAM256 | QAM1024
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:DUMD:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationD)

	def set_modulation(self, modulation: enums.ModulationD) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:MODulation \n
		Selects modulation for dummy data. \n
			:param modulation: QPSK| QAM16| QAM64 | QAM256 | QAM1024
		"""
		param = Conversions.enum_scalar_to_str(modulation, enums.ModulationD)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DUMD:MODulation {param}')

	def get_op_sub_frames(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:OPSubframes \n
		If the OCNG is used, you can disable (omit) the OCNG transmission in the non-muted PRS subframes. \n
			:return: omit_prs_sf: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:DUMD:OPSubframes?')
		return Conversions.str_to_bool(response)

	def set_op_sub_frames(self, omit_prs_sf: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:OPSubframes \n
		If the OCNG is used, you can disable (omit) the OCNG transmission in the non-muted PRS subframes. \n
			:param omit_prs_sf: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(omit_prs_sf)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DUMD:OPSubframes {param}')

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: bit pattern
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def get_pattern(self) -> PatternStruct:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:PATTern \n
		Sets the bit pattern. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:EUTRa:DL:DUMD:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:PATTern \n
		Sets the bit pattern. \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:EUTRa:DL:DUMD:PATTern', value)

	def get_power(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:POWer \n
		Sets the power for dummy data. \n
			:return: power: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:DUMD:POWer?')
		return Conversions.str_to_float(response)

	def set_power(self, power: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DUMD:POWer \n
		Sets the power for dummy data. \n
			:param power: float Range: -80 to 10
		"""
		param = Conversions.decimal_value_to_str(power)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DUMD:POWer {param}')
