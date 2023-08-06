from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IcPhase:
	"""IcPhase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("icPhase", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, vehicle=repcap.Vehicle.Default, antenna=repcap.Antenna.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:MPATh:[V<US>]:[A<GR>]:LOS:ICPHase \n
		Sets an initial code phase for the selected echo. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:return: init_code_phase: float Range: 0 to 3000, Unit: m"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		vehicle_cmd_val = self._base.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:MPATh:V{vehicle_cmd_val}:A{antenna_cmd_val}:LOS:ICPHase?')
		return Conversions.str_to_float(response)
