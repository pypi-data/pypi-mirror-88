from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Start:
	"""Start commands group definition. 39 total commands, 9 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("start", core, parent)

	def clone(self) -> 'Start':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Start(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def beidou(self):
		"""beidou commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .Start_.Beidou import Beidou
			self._beidou = Beidou(self._core, self._base)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Start_.Galileo import Galileo
			self._galileo = Galileo(self._core, self._base)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .Start_.Glonass import Glonass
			self._glonass = Glonass(self._core, self._base)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .Start_.Gps import Gps
			self._gps = Gps(self._core, self._base)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .Start_.Navic import Navic
			self._navic = Navic(self._core, self._base)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .Start_.Qzss import Qzss
			self._qzss = Qzss(self._core, self._base)
		return self._qzss

	@property
	def sbas(self):
		"""sbas commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbas'):
			from .Start_.Sbas import Sbas
			self._sbas = Sbas(self._core, self._base)
		return self._sbas

	@property
	def scTime(self):
		"""scTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scTime'):
			from .Start_.ScTime import ScTime
			self._scTime = ScTime(self._core, self._base)
		return self._scTime

	@property
	def utc(self):
		"""utc commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_utc'):
			from .Start_.Utc import Utc
			self._utc = Utc(self._core, self._base)
		return self._utc

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
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:DATE \n
		If the time base is UTC, defines the date for the simulation in DD.MM.YYYY format of the Gregorian calendar. \n
			:return: structure: for return value, see the help for DateStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:TIME:STARt:DATE?', self.__class__.DateStruct())

	def set_date(self, value: DateStruct) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:DATE \n
		If the time base is UTC, defines the date for the simulation in DD.MM.YYYY format of the Gregorian calendar. \n
			:param value: see the help for DateStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:GNSS:TIME:STARt:DATE', value)

	# noinspection PyTypeChecker
	def get_tbasis(self) -> enums.TimeBasis:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:TBASis \n
		Determines the time basis used to enter the simulation start time. \n
			:return: system_time: UTC| GPS| GST| GLO| BDT| NAV
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:TBASis?')
		return Conversions.str_to_scalar_enum(response, enums.TimeBasis)

	def set_tbasis(self, system_time: enums.TimeBasis) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:TBASis \n
		Determines the time basis used to enter the simulation start time. \n
			:param system_time: UTC| GPS| GST| GLO| BDT| NAV
		"""
		param = Conversions.enum_scalar_to_str(system_time, enums.TimeBasis)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:TBASis {param}')

	# noinspection PyTypeChecker
	class TimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Hour: int: integer Range: 0 to 23
			- Minute: int: integer Range: 0 to 59
			- Second: float: float Range: 0 to 59.999"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_float('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None
			self.Second: float = None

	def get_time(self) -> TimeStruct:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:TIME \n
		If the time base is UTC, sets the simulation start time in UTC time format. \n
			:return: structure: for return value, see the help for TimeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:TIME:STARt:TIME?', self.__class__.TimeStruct())

	def set_time(self, value: TimeStruct) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:TIME \n
		If the time base is UTC, sets the simulation start time in UTC time format. \n
			:param value: see the help for TimeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:GNSS:TIME:STARt:TIME', value)

	def get_to_week(self) -> float:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:TOWeek \n
		If time base is GPS or GST, sets the simulation start time within week set with the command method RsSmbv.Source.Bb.Gnss.
		Time.Start.wnumber. \n
			:return: tow: float Number of seconds since the beginning of the week Range: 0 to 604799.999
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:TOWeek?')
		return Conversions.str_to_float(response)

	def set_to_week(self, tow: float) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:TOWeek \n
		If time base is GPS or GST, sets the simulation start time within week set with the command method RsSmbv.Source.Bb.Gnss.
		Time.Start.wnumber. \n
			:param tow: float Number of seconds since the beginning of the week Range: 0 to 604799.999
		"""
		param = Conversions.decimal_value_to_str(tow)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:TOWeek {param}')

	def get_wnumber(self) -> int:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:WNUMber \n
		If time base is GPS or GST, sets the week number (WN) . \n
			:return: week: integer The weeks are numbered starting from a reference time point (WN_REF=0) , that depends on the navigation standard. Range: 0 to 9999*53
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:STARt:WNUMber?')
		return Conversions.str_to_int(response)

	def set_wnumber(self, week: int) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:STARt:WNUMber \n
		If time base is GPS or GST, sets the week number (WN) . \n
			:param week: integer The weeks are numbered starting from a reference time point (WN_REF=0) , that depends on the navigation standard. Range: 0 to 9999*53
		"""
		param = Conversions.decimal_value_to_str(week)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:STARt:WNUMber {param}')
