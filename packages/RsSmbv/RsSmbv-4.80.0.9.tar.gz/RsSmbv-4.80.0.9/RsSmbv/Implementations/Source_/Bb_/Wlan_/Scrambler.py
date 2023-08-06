from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scrambler:
	"""Scrambler commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scrambler", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.WlanScrMode:
		"""[SOURce<HW>]:BB:WLAN:SCRambler:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:SCRambler:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.WlanScrMode)

	def set_mode(self, mode: enums.WlanScrMode) -> None:
		"""[SOURce<HW>]:BB:WLAN:SCRambler:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.WlanScrMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:SCRambler:MODE {param}')

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: No parameter help available
			- Bit_Count: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def get_pattern(self) -> PatternStruct:
		"""[SOURce<HW>]:BB:WLAN:SCRambler:PATTern \n
		No command help available \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:WLAN:SCRambler:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""[SOURce<HW>]:BB:WLAN:SCRambler:PATTern \n
		No command help available \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:WLAN:SCRambler:PATTern', value)
