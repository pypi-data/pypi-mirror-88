from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Date:
	"""Date commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("date", core, parent)

	# noinspection PyTypeChecker
	class DateStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
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

	def set(self, structure: DateStruct, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GLONass<ST>:TOAData:DATE \n
		Enabled for UTC or GLONASS timebase (method RsSmbv.Source.Bb.Gnss.AdGeneration.Gps.ToaData.Tbasis.set) . Enters the date
		for the assistance data in DMS format of the Gregorian calendar. \n
			:param structure: for set value, see the help for DateStruct structure arguments.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass{stream_cmd_val}:TOAData:DATE', structure)

	def get(self, stream=repcap.Stream.Default) -> DateStruct:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GLONass<ST>:TOAData:DATE \n
		Enabled for UTC or GLONASS timebase (method RsSmbv.Source.Bb.Gnss.AdGeneration.Gps.ToaData.Tbasis.set) . Enters the date
		for the assistance data in DMS format of the Gregorian calendar. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: structure: for return value, see the help for DateStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass{stream_cmd_val}:TOAData:DATE?', self.__class__.DateStruct())
