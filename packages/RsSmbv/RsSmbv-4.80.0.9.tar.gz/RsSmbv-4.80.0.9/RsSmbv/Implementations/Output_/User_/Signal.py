from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Signal:
	"""Signal commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("signal", core, parent)

	def set(self, signal: enums.OutpConnGlbSignal, channel=repcap.Channel.Default) -> None:
		"""OUTPut<HW>:USER<CH>:SIGNal \n
		Sets the control signal that is output at the selected connector. To define the connector direction, use the command
		method RsSmbv.Output.User.Direction.set. \n
			:param signal: MARKA1| MARKA2| MARKA3| NONE| SYNCOUT| SCLock| LATTenuation| BGATe| HOP| CWMODulation| TRIGgered| MTRigger| LOW| HIGH | BERRESTOUT| BERDATENOUT| BERCLKOUT| BERDATOUT MARKA1|2|3 = Baseband Marker 1/2/3 MTRigger = Manual Trigger, available for USER5 BERRESTOUT|BERDATENOUT|BERCLKOUT|BERDATOUT = BER TestGen Data, Clock, Data Enable and Restart SYNCOUT = Baseband Sync Out SCLock = Symbol Clock LATTenuation = Lev Att BGATA = Burst Gate HOP = HOP CWMODulation = CW/Mod TRIGgered = Triggered MTRigger = Manual Trigger, available for USER5 LOW|HIGH = Always 0/1 NONE = none
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(signal, enums.OutpConnGlbSignal)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'OUTPut<HwInstance>:USER{channel_cmd_val}:SIGNal {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.OutpConnGlbSignal:
		"""OUTPut<HW>:USER<CH>:SIGNal \n
		Sets the control signal that is output at the selected connector. To define the connector direction, use the command
		method RsSmbv.Output.User.Direction.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: signal: MARKA1| MARKA2| MARKA3| NONE| SYNCOUT| SCLock| LATTenuation| BGATe| HOP| CWMODulation| TRIGgered| MTRigger| LOW| HIGH | BERRESTOUT| BERDATENOUT| BERCLKOUT| BERDATOUT MARKA1|2|3 = Baseband Marker 1/2/3 MTRigger = Manual Trigger, available for USER5 BERRESTOUT|BERDATENOUT|BERCLKOUT|BERDATOUT = BER TestGen Data, Clock, Data Enable and Restart SYNCOUT = Baseband Sync Out SCLock = Symbol Clock LATTenuation = Lev Att BGATA = Burst Gate HOP = HOP CWMODulation = CW/Mod TRIGgered = Triggered MTRigger = Manual Trigger, available for USER5 LOW|HIGH = Always 0/1 NONE = none"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'OUTPut<HwInstance>:USER{channel_cmd_val}:SIGNal?')
		return Conversions.str_to_scalar_enum(response, enums.OutpConnGlbSignal)
