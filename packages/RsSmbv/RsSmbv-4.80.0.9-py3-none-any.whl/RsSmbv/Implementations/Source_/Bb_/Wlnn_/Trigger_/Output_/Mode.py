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

	def set(self, mode: enums.WlannMarkMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param mode: RESTart| FBLock| FRAMe| FAPart| PULSe| PATTern| RATio| FIPart RESTart A marker signal is generated at the start of each signal sequence (period = all frame blocks) . FRAMe Number of Frame Blocks = 1, that is, a marker signal is generated at the start of each frame in the single frame block. Otherwise, the frame block and frame index are entered and the specific frame is masked. FBLock Number of Frame Blocks = 1, that is, a marker signal is generated at the start of each frame block. Otherwise, a specific frame block index is given and the whole frame block is marked. FAPart Number of Frame Blocks = 1, that is, a marker signal is generated to mark every active part of each frame. The active data transfer part (PPDU) of a frame period is marked with high, the inactive part (idle time) with low. This marker can be used to decrease the carrier leakage during inactive signal parts by feeding it into the pulse modulator. Otherwise, the frame block and frame index are entered and the active part of the specific frame is masked. PATTern A marker signal is generated according to the user defined pattern (command SOURce:BB:WLNN:TRIGger:OUTPut:PATTern) . PULSe A pulsed marker signal is generated. The pulse frequency (= symbol rate/divider) is defined with the SOUR:BB:WLNN:TRIG:OUTP:PULSe:DIVider command and can be queried with the SOUR:BB:WLNN:TRIG:OUTP:PULSe:FREQuency? command. RATio A marker signal corresponding to the Time Off / Time On specifications in the commands SOURce:BB:WLNN:TRIGger:OUTPut:OFFT and 'SOURce:BB:WLNN:TRIGger:OUTPut:ONT' is generated.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.WlannMarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannMarkMode:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut<CH>:MODE \n
		Defines the signal for the selected marker output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: RESTart| FBLock| FRAMe| FAPart| PULSe| PATTern| RATio| FIPart RESTart A marker signal is generated at the start of each signal sequence (period = all frame blocks) . FRAMe Number of Frame Blocks = 1, that is, a marker signal is generated at the start of each frame in the single frame block. Otherwise, the frame block and frame index are entered and the specific frame is masked. FBLock Number of Frame Blocks = 1, that is, a marker signal is generated at the start of each frame block. Otherwise, a specific frame block index is given and the whole frame block is marked. FAPart Number of Frame Blocks = 1, that is, a marker signal is generated to mark every active part of each frame. The active data transfer part (PPDU) of a frame period is marked with high, the inactive part (idle time) with low. This marker can be used to decrease the carrier leakage during inactive signal parts by feeding it into the pulse modulator. Otherwise, the frame block and frame index are entered and the active part of the specific frame is masked. PATTern A marker signal is generated according to the user defined pattern (command SOURce:BB:WLNN:TRIGger:OUTPut:PATTern) . PULSe A pulsed marker signal is generated. The pulse frequency (= symbol rate/divider) is defined with the SOUR:BB:WLNN:TRIG:OUTP:PULSe:DIVider command and can be queried with the SOUR:BB:WLNN:TRIG:OUTP:PULSe:FREQuency? command. RATio A marker signal corresponding to the Time Off / Time On specifications in the commands SOURce:BB:WLNN:TRIGger:OUTPut:OFFT and 'SOURce:BB:WLNN:TRIGger:OUTPut:ONT' is generated."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.WlannMarkMode)
