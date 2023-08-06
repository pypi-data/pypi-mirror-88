from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Signal:
	"""Signal commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("signal", core, parent)

	def set(self, signal: enums.InpOutpConnGlbMapSign, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:INPut:USER<CH>:SIGNal \n
		Determines the control signal that is input at the selected connector. To define the connector direction, use the command
		method RsSmbv.Source.InputPy.User.Direction.set. \n
			:param signal: TRIG1| CLOCK1| NSEGM1| NONE| SYNCIN | BERDATIN| BERCLKIN| BERDATENIN| BERRESTIN TRIG1 = Global Trigger CLOCK1 = Global Clock NSEGM1 = Global Next Segment SYNCIN = Baseband Sync In BERDATIN|BERCLKIN|BERDATENIN|BERRESTIN = BER Data, Clock, Data Enable and Restart NONE = none
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(signal, enums.InpOutpConnGlbMapSign)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:INPut:USER{channel_cmd_val}:SIGNal {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.InpOutpConnGlbMapSign:
		"""[SOURce]:INPut:USER<CH>:SIGNal \n
		Determines the control signal that is input at the selected connector. To define the connector direction, use the command
		method RsSmbv.Source.InputPy.User.Direction.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: signal: TRIG1| CLOCK1| NSEGM1| NONE| SYNCIN | BERDATIN| BERCLKIN| BERDATENIN| BERRESTIN TRIG1 = Global Trigger CLOCK1 = Global Clock NSEGM1 = Global Next Segment SYNCIN = Baseband Sync In BERDATIN|BERCLKIN|BERDATENIN|BERRESTIN = BER Data, Clock, Data Enable and Restart NONE = none"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:INPut:USER{channel_cmd_val}:SIGNal?')
		return Conversions.str_to_scalar_enum(response, enums.InpOutpConnGlbMapSign)
