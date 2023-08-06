from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 34 total commands, 8 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("display", core, parent)

	def clone(self) -> 'Display':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Display(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def antenna(self):
		"""antenna commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_antenna'):
			from .Display_.Antenna import Antenna
			self._antenna = Antenna(self._core, self._base)
		return self._antenna

	@property
	def channels(self):
		"""channels commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_channels'):
			from .Display_.Channels import Channels
			self._channels = Channels(self._core, self._base)
		return self._channels

	@property
	def map(self):
		"""map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_map'):
			from .Display_.Map import Map
			self._map = Map(self._core, self._base)
		return self._map

	@property
	def power(self):
		"""power commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Display_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def stream(self):
		"""stream commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stream'):
			from .Display_.Stream import Stream
			self._stream = Stream(self._core, self._base)
		return self._stream

	@property
	def tracks(self):
		"""tracks commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tracks'):
			from .Display_.Tracks import Tracks
			self._tracks = Tracks(self._core, self._base)
		return self._tracks

	@property
	def trajectory(self):
		"""trajectory commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_trajectory'):
			from .Display_.Trajectory import Trajectory
			self._trajectory = Trajectory(self._core, self._base)
		return self._trajectory

	@property
	def vehicle(self):
		"""vehicle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vehicle'):
			from .Display_.Vehicle import Vehicle
			self._vehicle = Vehicle(self._core, self._base)
		return self._vehicle

	def set(self, display_type: enums.MonitorDisplayType, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay \n
		Switches between the available views. \n
			:param display_type: SKY| MAP| POWer| TRAJectory| ATTitude| TRACks| CHANnels
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')"""
		param = Conversions.enum_scalar_to_str(display_type, enums.MonitorDisplayType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MonitorDisplayType:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay \n
		Switches between the available views. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:return: display_type: SKY| MAP| POWer| TRAJectory| ATTitude| TRACks| CHANnels"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay?')
		return Conversions.str_to_scalar_enum(response, enums.MonitorDisplayType)
