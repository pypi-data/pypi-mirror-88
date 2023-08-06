from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 11 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	def clone(self) -> 'Time':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Time(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def daylightSavingTime(self):
		"""daylightSavingTime commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_daylightSavingTime'):
			from .Time_.DaylightSavingTime import DaylightSavingTime
			self._daylightSavingTime = DaylightSavingTime(self._core, self._base)
		return self._daylightSavingTime

	@property
	def hrTimer(self):
		"""hrTimer commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_hrTimer'):
			from .Time_.HrTimer import HrTimer
			self._hrTimer = HrTimer(self._core, self._base)
		return self._hrTimer

	@property
	def zone(self):
		"""zone commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_zone'):
			from .Time_.Zone import Zone
			self._zone = Zone(self._core, self._base)
		return self._zone

	def get_local(self) -> str:
		"""SYSTem:TIME:LOCal \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:LOCal?')
		return trim_str_response(response)

	def set_local(self, pseudo_string: str) -> None:
		"""SYSTem:TIME:LOCal \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TIME:LOCal {param}')

	def get_utc(self) -> str:
		"""SYSTem:TIME:UTC \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:UTC?')
		return trim_str_response(response)

	def set_utc(self, pseudo_string: str) -> None:
		"""SYSTem:TIME:UTC \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TIME:UTC {param}')

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Hour: List[int]: integer Range: 0 to 23
			- Minute: int: integer Range: 0 to 59
			- Second: int: integer Range: 0 to 59"""
		__meta_args_list = [
			ArgStruct('Hour', DataType.IntegerList, None, False, True, 1),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_int('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: List[int] = None
			self.Minute: int = None
			self.Second: int = None

	def get_value(self) -> ValueStruct:
		"""SYSTem:TIME \n
		Queries or sets the time for the instrument-internal clock. This is a password-protected function. Unlock the protection
		level 1 to access it. See SYSTem. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:TIME?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SYSTem:TIME \n
		Queries or sets the time for the instrument-internal clock. This is a password-protected function. Unlock the protection
		level 1 to access it. See SYSTem. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:TIME', value)
