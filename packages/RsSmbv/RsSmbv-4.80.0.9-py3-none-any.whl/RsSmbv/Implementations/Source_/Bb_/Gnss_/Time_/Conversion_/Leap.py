from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Leap:
	"""Leap commands group definition. 4 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("leap", core, parent)

	def clone(self) -> 'Leap':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Leap(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def seconds(self):
		"""seconds commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_seconds'):
			from .Leap_.Seconds import Seconds
			self._seconds = Seconds(self._core, self._base)
		return self._seconds

	def get_auto(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:LEAP:AUTO \n
		Enables the simulation of the leap second transition. \n
			:return: auto_configure: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:LEAP:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, auto_configure: bool) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:LEAP:AUTO \n
		Enables the simulation of the leap second transition. \n
			:param auto_configure: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(auto_configure)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:LEAP:AUTO {param}')

	# noinspection PyTypeChecker
	class DateStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Year: int: integer Range: 1980 to 9999
			- Month: int: integer Range: 1 to 12
			- Day: int: integer Range: 1 to 31"""
		__meta_args_list = [
			ArgStruct.scalar_int('Year'),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None

	def get_date(self) -> DateStruct:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:LEAP:DATE \n
		Defines the date of the next UTC time correction. \n
			:return: structure: for return value, see the help for DateStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:LEAP:DATE?', self.__class__.DateStruct())

	def set_date(self, value: DateStruct) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:LEAP:DATE \n
		Defines the date of the next UTC time correction. \n
			:param value: see the help for DateStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:LEAP:DATE', value)
