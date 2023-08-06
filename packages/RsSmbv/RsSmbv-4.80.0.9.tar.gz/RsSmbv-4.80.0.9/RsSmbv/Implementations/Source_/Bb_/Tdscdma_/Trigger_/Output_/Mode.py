from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.TdscdmaMarkMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param mode: RFRame| SFNR| CSPeriod| RATio| USER| FACTive RFRame = Radio Frame SFNR = System Frame Number (SFN) Restart CSPeriod = Chip Sequence Period (ARB) RATio = On/Off Ratio USER = User Period
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.TdscdmaMarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.TdscdmaMarkMode:
		"""[SOURce<HW>]:BB:TDSCdma:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: RFRame| SFNR| CSPeriod| RATio| USER| FACTive RFRame = Radio Frame SFNR = System Frame Number (SFN) Restart CSPeriod = Chip Sequence Period (ARB) RATio = On/Off Ratio USER = User Period"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaMarkMode)
