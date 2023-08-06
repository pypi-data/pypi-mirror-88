from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def set(self, frequency: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:LFOutput<CH>:FREQuency \n
		Sets the frequency of the LF signal in method RsSmbv.Source.LfOutput.Frequency.mode CW|FIXed mode.
			INTRO_CMD_HELP: Note \n
			- If signal source 'Internal' is set, the instrument performs the analog modulations (AM/FM/PhiM/PM) with this frequency.
			- In sweep mode (method RsSmbv.Source.LfOutput.Frequency.mode SWE) , the frequency is coupled with the sweep frequency. \n
			:param frequency: float Range: depends on the installed options , Unit: Hz
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')"""
		param = Conversions.decimal_value_to_str(frequency)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:LFOutput{channel_cmd_val}:FREQuency {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce]:LFOutput<CH>:FREQuency \n
		Sets the frequency of the LF signal in method RsSmbv.Source.LfOutput.Frequency.mode CW|FIXed mode.
			INTRO_CMD_HELP: Note \n
			- If signal source 'Internal' is set, the instrument performs the analog modulations (AM/FM/PhiM/PM) with this frequency.
			- In sweep mode (method RsSmbv.Source.LfOutput.Frequency.mode SWE) , the frequency is coupled with the sweep frequency. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')
			:return: frequency: float Range: depends on the installed options , Unit: Hz"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:LFOutput{channel_cmd_val}:FREQuency?')
		return Conversions.str_to_float(response)

	def get_manual(self) -> float:
		"""[SOURce<HW>]:LFOutput:FREQuency:MANual \n
		Sets the frequency of the subsequent sweep step if LFO:SWE:MODE MAN. Use a separate command for each sweep step. \n
			:return: manual: float You can select any value within the setting range, where: STARt is set with method RsSmbv.Source.LfOutput.Frequency.start STOP is set with method RsSmbv.Source.LfOutput.Frequency.stop Range: STARt to STOP
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:FREQuency:MANual?')
		return Conversions.str_to_float(response)

	def set_manual(self, manual: float) -> None:
		"""[SOURce<HW>]:LFOutput:FREQuency:MANual \n
		Sets the frequency of the subsequent sweep step if LFO:SWE:MODE MAN. Use a separate command for each sweep step. \n
			:param manual: float You can select any value within the setting range, where: STARt is set with method RsSmbv.Source.LfOutput.Frequency.start STOP is set with method RsSmbv.Source.LfOutput.Frequency.stop Range: STARt to STOP
		"""
		param = Conversions.decimal_value_to_str(manual)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:FREQuency:MANual {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.LfFreqMode:
		"""[SOURce<HW>]:LFOutput:FREQuency:MODE \n
		Sets the mode for the output of the LF generator frequency, and determines the commands to be used for frequency settings. \n
			:return: mode: CW| FIXed| SWEep CW|FIXed Sets the fixed-frequency mode. CW and FIXed are synonyms. To set the output frequency, use command method RsSmbv.Source.LfOutput.Frequency.set SWEep Sets sweep mode. To set the frequency, use the commands: method RsSmbv.Source.LfOutput.Frequency.start and method RsSmbv.Source.LfOutput.Frequency.stop Or method RsSmbv.Source.LfOutput.Frequency.manual
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.LfFreqMode)

	def set_mode(self, mode: enums.LfFreqMode) -> None:
		"""[SOURce<HW>]:LFOutput:FREQuency:MODE \n
		Sets the mode for the output of the LF generator frequency, and determines the commands to be used for frequency settings. \n
			:param mode: CW| FIXed| SWEep CW|FIXed Sets the fixed-frequency mode. CW and FIXed are synonyms. To set the output frequency, use command method RsSmbv.Source.LfOutput.Frequency.set SWEep Sets sweep mode. To set the frequency, use the commands: method RsSmbv.Source.LfOutput.Frequency.start and method RsSmbv.Source.LfOutput.Frequency.stop Or method RsSmbv.Source.LfOutput.Frequency.manual
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.LfFreqMode)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:FREQuency:MODE {param}')

	def get_start(self) -> float:
		"""[SOURce<HW>]:LFOutput:FREQuency:STARt \n
		Sets the start/stop frequency for method RsSmbv.Source.LfOutput.Frequency.mode SWEep. \n
			:return: start: float Range: 0.1 Hz to 1 MHz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:FREQuency:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start: float) -> None:
		"""[SOURce<HW>]:LFOutput:FREQuency:STARt \n
		Sets the start/stop frequency for method RsSmbv.Source.LfOutput.Frequency.mode SWEep. \n
			:param start: float Range: 0.1 Hz to 1 MHz
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:FREQuency:STARt {param}')

	def get_stop(self) -> float:
		"""[SOURce<HW>]:LFOutput:FREQuency:STOP \n
		Sets the start/stop frequency for method RsSmbv.Source.LfOutput.Frequency.mode SWEep. \n
			:return: stop: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:FREQuency:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, stop: float) -> None:
		"""[SOURce<HW>]:LFOutput:FREQuency:STOP \n
		Sets the start/stop frequency for method RsSmbv.Source.LfOutput.Frequency.mode SWEep. \n
			:param stop: float Range: 0.1 Hz to 1 MHz
		"""
		param = Conversions.decimal_value_to_str(stop)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:FREQuency:STOP {param}')
