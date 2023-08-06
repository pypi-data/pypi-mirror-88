from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dms:
	"""Dms commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dms", core, parent)

	# noinspection PyTypeChecker
	class DmsStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Longitude_Deg: int: integer Range: 0 to 180
			- Longitude_Min: int: integer Defines the longitude minutes. Range: 0 to 59
			- Longitude_Sec: float: float Defines the longitude seconds. Range: 0 to 59.999
			- Longitude_Dir: str: EAST | WEST Defines the longitude direction.
			- Latitude_Deg: int: integer Defines the latitude degrees. Range: 0 to 90
			- Latitude_Min: int: integer Defines the latitude minutes. Range: 0 to 59
			- Latitude_Sec: float: float Defines the latitude seconds. Range: 0 to 59.999
			- Latitude_Dir: str: NORTh | SOUTh Defines the latitude direction."""
		__meta_args_list = [
			ArgStruct.scalar_int('Longitude_Deg'),
			ArgStruct.scalar_int('Longitude_Min'),
			ArgStruct.scalar_float('Longitude_Sec'),
			ArgStruct.scalar_str('Longitude_Dir'),
			ArgStruct.scalar_int('Latitude_Deg'),
			ArgStruct.scalar_int('Latitude_Min'),
			ArgStruct.scalar_float('Latitude_Sec'),
			ArgStruct.scalar_str('Latitude_Dir')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude_Deg: int = None
			self.Longitude_Min: int = None
			self.Longitude_Sec: float = None
			self.Longitude_Dir: str = None
			self.Latitude_Deg: int = None
			self.Latitude_Min: int = None
			self.Latitude_Sec: float = None
			self.Latitude_Dir: str = None

	def set(self, structure: DmsStruct, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:LFLocation:COORdinates:DMS \n
		Defines the coordinates of the LTP/FTP in degrees, minutes and seconds. \n
			:param structure: for set value, see the help for DmsStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:LFLocation:COORdinates:DMS', structure)

	def get(self, channel=repcap.Channel.Default) -> DmsStruct:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:LFLocation:COORdinates:DMS \n
		Defines the coordinates of the LTP/FTP in degrees, minutes and seconds. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: structure: for return value, see the help for DmsStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:LFLocation:COORdinates:DMS?', self.__class__.DmsStruct())
