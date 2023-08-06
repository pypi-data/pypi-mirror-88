from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pz:
	"""Pz commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pz", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Pz':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pz(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class PzStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Longitude_Deg: int: integer Range: 0 to 180
			- Longitude_Min: int: integer Range: 0 to 59
			- Longitude_Sec: float: float Range: 0 to 59.999
			- Longitude_Dir: str: select
			- Latitude_Deg: int: integer Range: 0 to 90
			- Latitude_Min: int: integer Range: 0 to 59
			- Latitude_Sec: float: float Range: 0 to 59.999
			- Latitude_Dir: str: select
			- Altitude: float: float Range: -10E3 to 50E6"""
		__meta_args_list = [
			ArgStruct.scalar_int('Longitude_Deg'),
			ArgStruct.scalar_int('Longitude_Min'),
			ArgStruct.scalar_float('Longitude_Sec'),
			ArgStruct.scalar_str('Longitude_Dir'),
			ArgStruct.scalar_int('Latitude_Deg'),
			ArgStruct.scalar_int('Latitude_Min'),
			ArgStruct.scalar_float('Latitude_Sec'),
			ArgStruct.scalar_str('Latitude_Dir'),
			ArgStruct.scalar_float('Altitude')]

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
			self.Altitude: float = None

	def set(self, structure: PzStruct, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GPS<ST>:LOCation:COORdinates:DMS:PZ<CH> \n
		Sets the geographic reference location in degrees, minutes and seconds. \n
			:param structure: for set value, see the help for PzStruct structure arguments.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pz')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS{stream_cmd_val}:LOCation:COORdinates:DMS:PZ{channel_cmd_val}', structure)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> PzStruct:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GPS<ST>:LOCation:COORdinates:DMS:PZ<CH> \n
		Sets the geographic reference location in degrees, minutes and seconds. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pz')
			:return: structure: for return value, see the help for PzStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS{stream_cmd_val}:LOCation:COORdinates:DMS:PZ{channel_cmd_val}?', self.__class__.PzStruct())
