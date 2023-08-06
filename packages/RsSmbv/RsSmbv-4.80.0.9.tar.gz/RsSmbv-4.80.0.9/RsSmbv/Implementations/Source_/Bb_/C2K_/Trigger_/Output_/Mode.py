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

	def set(self, mode: enums.Cdma2KmarkMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param mode: PCGRoup| RFRame| SCFRame| SFRame| ESECond| CSPeriod| RATio| USER Marker signal that marks: PCGRoup The start of each power control group (every 1.25 ms) . RFRame Every 20 ms (traffic channel clock) . SCFRame The start of each sync channel frame (every 26.6 ms) . SFRame Every 80 ms (super frame clock) . ESECond Every 2 s (even second mark) . CSPeriod The start of each arbitrary waveform sequence RATio Off / On times USER The beginning of every user-defined period
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.Cdma2KmarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.Cdma2KmarkMode:
		"""[SOURce<HW>]:BB:C2K:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: PCGRoup| RFRame| SCFRame| SFRame| ESECond| CSPeriod| RATio| USER Marker signal that marks: PCGRoup The start of each power control group (every 1.25 ms) . RFRame Every 20 ms (traffic channel clock) . SCFRame The start of each sync channel frame (every 26.6 ms) . SFRame Every 80 ms (super frame clock) . ESECond Every 2 s (even second mark) . CSPeriod The start of each arbitrary waveform sequence RATio Off / On times USER The beginning of every user-defined period"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KmarkMode)
