from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Imaginary:
	"""Imaginary commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("imaginary", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Imaginary':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Imaginary(self._core, self._base.parent)
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

	def set(self, ant_port_map_dat: float, antennaPort=repcap.AntennaPort.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:APM:CS:AP<DIR>:ROW<ST>:IMAGinary<CH> \n
		Define the mapping of the antenna ports to the physical antennas. \n
			:param ant_port_map_dat: float The REAL (Magnitude) and IMAGinary (Phase) values are interdependent. Their value ranges change depending on each other and so that the resulting complex value is as follows: |REAL+j*IMAGinary| ≤ 1 Otherwise, the values are normalized to Magnitude = 1. Range: -1 to 360
			:param antennaPort: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Ap')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Imaginary')"""
		param = Conversions.decimal_value_to_str(ant_port_map_dat)
		antennaPort_cmd_val = self._base.get_repcap_cmd_value(antennaPort, repcap.AntennaPort)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MIMO:APM:CS:AP{antennaPort_cmd_val}:ROW{stream_cmd_val}:IMAGinary{channel_cmd_val} {param}')

	def get(self, antennaPort=repcap.AntennaPort.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:APM:CS:AP<DIR>:ROW<ST>:IMAGinary<CH> \n
		Define the mapping of the antenna ports to the physical antennas. \n
			:param antennaPort: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Ap')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Imaginary')
			:return: ant_port_map_dat: float The REAL (Magnitude) and IMAGinary (Phase) values are interdependent. Their value ranges change depending on each other and so that the resulting complex value is as follows: |REAL+j*IMAGinary| ≤ 1 Otherwise, the values are normalized to Magnitude = 1. Range: -1 to 360"""
		antennaPort_cmd_val = self._base.get_repcap_cmd_value(antennaPort, repcap.AntennaPort)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MIMO:APM:CS:AP{antennaPort_cmd_val}:ROW{stream_cmd_val}:IMAGinary{channel_cmd_val}?')
		return Conversions.str_to_float(response)
