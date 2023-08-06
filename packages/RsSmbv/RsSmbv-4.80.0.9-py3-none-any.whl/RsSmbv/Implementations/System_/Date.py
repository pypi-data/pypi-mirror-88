from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Date:
	"""Date commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("date", core, parent)

	def get_local(self) -> str:
		"""SYSTem:DATE:LOCal \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:DATE:LOCal?')
		return trim_str_response(response)

	def set_local(self, pseudo_string: str) -> None:
		"""SYSTem:DATE:LOCal \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:DATE:LOCal {param}')

	def get_utc(self) -> str:
		"""SYSTem:DATE:UTC \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:DATE:UTC?')
		return trim_str_response(response)

	def set_utc(self, pseudo_string: str) -> None:
		"""SYSTem:DATE:UTC \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:DATE:UTC {param}')

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Year: List[int]: integer
			- Month: int: integer Range: 1 to 12
			- Day: int: integer Range: 1 to 31"""
		__meta_args_list = [
			ArgStruct('Year', DataType.IntegerList, None, False, True, 1),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: List[int] = None
			self.Month: int = None
			self.Day: int = None

	def get_value(self) -> ValueStruct:
		"""SYSTem:DATE \n
		Queries or sets the date for the instrument-internal calendar. This is a password-protected function.
		Unlock the protection level 1 to access it. See SYSTem. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:DATE?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SYSTem:DATE \n
		Queries or sets the date for the instrument-internal calendar. This is a password-protected function.
		Unlock the protection level 1 to access it. See SYSTem. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:DATE', value)
