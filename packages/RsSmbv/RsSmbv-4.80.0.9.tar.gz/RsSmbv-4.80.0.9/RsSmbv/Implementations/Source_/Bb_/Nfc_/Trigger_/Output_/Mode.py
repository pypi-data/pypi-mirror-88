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

	def set(self, mode: enums.TriggerMarkModeB, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:TRIGger:OUTPut<CH>:MODE \n
		No command help available \n
			:param mode: PULSe| RESTart| PATTern| RATio PULSe A regular marker signal is generated. The frequency is derived by dividing the sample rate by the divider, which is input with the command method RsSmbv.Source.Bb.Nfc.Trigger.Output.Pulse.Divider.set. RESTart A marker signal is generated on every repetition of the complete frame sequence. PATTern A marker signal that is defined by a bit pattern is generated. The pattern has a maximum length of 64 bits and is defined with the commandmethod RsSmbv.Source.Bb.Nfc.Trigger.Output.Pattern.set RATio A marker signal corresponding to the Time Off / Time On specifications in the commands method RsSmbv.Source.Bb.Nfc.Trigger.Output.Ontime.set and method RsSmbv.Source.Bb.Nfc.Trigger.Output.OffTime.set
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.TriggerMarkModeB)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.TriggerMarkModeB:
		"""[SOURce<HW>]:BB:NFC:TRIGger:OUTPut<CH>:MODE \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: PULSe| RESTart| PATTern| RATio PULSe A regular marker signal is generated. The frequency is derived by dividing the sample rate by the divider, which is input with the command method RsSmbv.Source.Bb.Nfc.Trigger.Output.Pulse.Divider.set. RESTart A marker signal is generated on every repetition of the complete frame sequence. PATTern A marker signal that is defined by a bit pattern is generated. The pattern has a maximum length of 64 bits and is defined with the commandmethod RsSmbv.Source.Bb.Nfc.Trigger.Output.Pattern.set RATio A marker signal corresponding to the Time Off / Time On specifications in the commands method RsSmbv.Source.Bb.Nfc.Trigger.Output.Ontime.set and method RsSmbv.Source.Bb.Nfc.Trigger.Output.OffTime.set"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerMarkModeB)
