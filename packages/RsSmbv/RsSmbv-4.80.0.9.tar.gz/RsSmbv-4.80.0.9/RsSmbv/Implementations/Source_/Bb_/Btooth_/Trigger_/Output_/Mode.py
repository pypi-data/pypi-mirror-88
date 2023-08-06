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

	def set(self, mode: enums.BtoMarkMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:BTOoth:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param mode: RESTart| STARt| ACTive| PULSe| PATTern| RATio | IACTive RESTart A marker signal is generated at the start of each signal sequence. STARt A marker signal is generated at the start of each event/frame. ACTive The marker masks the active part of the event/frame. At the start of each burst, the marker signal changes to high. It changes back to low after the end of each burst. PULSe A regular marker signal is generated. The clock frequency is defined by entering a divider. The frequency is derived by dividing the symbol rate by the divider. The input box for divider opens when 'Pulse' is selected, and the resulting pulse frequency is displayed below. PATTern A marker signal that is defined by a bit pattern is generated. The pattern has a maximum length of 32 bits and is defined in an input field which opens when pattern is selected. RATio A regular marker signal corresponding to the'Time Off' / 'Time On' specifications in the commands :SOURce1:BB:BTO:TRIGger:OUTPut:OFFTime and :SOURce1:BB:BTO:TRIGger:OUTPut:ONTime is generated. IACTive The marker masks the inactive part of the event/frame. At the start of each burst, the marker signal changes to low. It changes back to high after the end of each burst.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.BtoMarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.BtoMarkMode:
		"""[SOURce<HW>]:BB:BTOoth:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: RESTart| STARt| ACTive| PULSe| PATTern| RATio | IACTive RESTart A marker signal is generated at the start of each signal sequence. STARt A marker signal is generated at the start of each event/frame. ACTive The marker masks the active part of the event/frame. At the start of each burst, the marker signal changes to high. It changes back to low after the end of each burst. PULSe A regular marker signal is generated. The clock frequency is defined by entering a divider. The frequency is derived by dividing the symbol rate by the divider. The input box for divider opens when 'Pulse' is selected, and the resulting pulse frequency is displayed below. PATTern A marker signal that is defined by a bit pattern is generated. The pattern has a maximum length of 32 bits and is defined in an input field which opens when pattern is selected. RATio A regular marker signal corresponding to the'Time Off' / 'Time On' specifications in the commands :SOURce1:BB:BTO:TRIGger:OUTPut:OFFTime and :SOURce1:BB:BTO:TRIGger:OUTPut:ONTime is generated. IACTive The marker masks the inactive part of the event/frame. At the start of each burst, the marker signal changes to low. It changes back to high after the end of each burst."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.BtoMarkMode)
