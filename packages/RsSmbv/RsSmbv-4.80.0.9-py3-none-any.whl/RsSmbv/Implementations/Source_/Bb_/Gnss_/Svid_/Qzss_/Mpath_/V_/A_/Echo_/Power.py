from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def set(self, power_offset: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, vehicle=repcap.Vehicle.Default, antenna=repcap.Antenna.Default, echoes=repcap.Echoes.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:MPATh:[V<US>]:[A<GR>]:ECHO<S2US>:POWer \n
		Sets the additional power offset for the selected echoes. \n
			:param power_offset: float Range: -15 to 0, Unit: dB
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:param echoes: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Echo')"""
		param = Conversions.decimal_value_to_str(power_offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		vehicle_cmd_val = self._base.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		echoes_cmd_val = self._base.get_repcap_cmd_value(echoes, repcap.Echoes)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:MPATh:V{vehicle_cmd_val}:A{antenna_cmd_val}:ECHO{echoes_cmd_val}:POWer {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, vehicle=repcap.Vehicle.Default, antenna=repcap.Antenna.Default, echoes=repcap.Echoes.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:MPATh:[V<US>]:[A<GR>]:ECHO<S2US>:POWer \n
		Sets the additional power offset for the selected echoes. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:param echoes: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Echo')
			:return: power_offset: float Range: -15 to 0, Unit: dB"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		vehicle_cmd_val = self._base.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		echoes_cmd_val = self._base.get_repcap_cmd_value(echoes, repcap.Echoes)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:MPATh:V{vehicle_cmd_val}:A{antenna_cmd_val}:ECHO{echoes_cmd_val}:POWer?')
		return Conversions.str_to_float(response)
