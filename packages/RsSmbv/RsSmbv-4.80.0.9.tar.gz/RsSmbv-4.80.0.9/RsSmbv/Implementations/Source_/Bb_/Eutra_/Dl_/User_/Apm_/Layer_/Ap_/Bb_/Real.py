from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Real:
	"""Real commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("real", core, parent)

	def set(self, ant_port_map_data: float, channel=repcap.Channel.Default, layer=repcap.Layer.Default, antennaPort=repcap.AntennaPort.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:APM:[LAYer<USER>]:AP<DIR>:BB<ST>:REAL \n
		Defines the mapping of the antenna ports to the physical antennas. \n
			:param ant_port_map_data: float The REAL (Magnitude) and IMAGinary (Phase) values are interdependent. Their value ranges change depending on each other and so that the resulting complex value is as follows: |REAL+j*IMAGinary| ≤ 1 Otherwise, the values are normalized to Magnitude = 1. Range: -1 to 360
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param layer: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Layer')
			:param antennaPort: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Ap')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bb')"""
		param = Conversions.decimal_value_to_str(ant_port_map_data)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		layer_cmd_val = self._base.get_repcap_cmd_value(layer, repcap.Layer)
		antennaPort_cmd_val = self._base.get_repcap_cmd_value(antennaPort, repcap.AntennaPort)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:APM:LAYer{layer_cmd_val}:AP{antennaPort_cmd_val}:BB{stream_cmd_val}:REAL {param}')

	def get(self, channel=repcap.Channel.Default, layer=repcap.Layer.Default, antennaPort=repcap.AntennaPort.Default, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:APM:[LAYer<USER>]:AP<DIR>:BB<ST>:REAL \n
		Defines the mapping of the antenna ports to the physical antennas. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param layer: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Layer')
			:param antennaPort: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Ap')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bb')
			:return: ant_port_map_data: float The REAL (Magnitude) and IMAGinary (Phase) values are interdependent. Their value ranges change depending on each other and so that the resulting complex value is as follows: |REAL+j*IMAGinary| ≤ 1 Otherwise, the values are normalized to Magnitude = 1. Range: -1 to 360"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		layer_cmd_val = self._base.get_repcap_cmd_value(layer, repcap.Layer)
		antennaPort_cmd_val = self._base.get_repcap_cmd_value(antennaPort, repcap.AntennaPort)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:APM:LAYer{layer_cmd_val}:AP{antennaPort_cmd_val}:BB{stream_cmd_val}:REAL?')
		return Conversions.str_to_float(response)
