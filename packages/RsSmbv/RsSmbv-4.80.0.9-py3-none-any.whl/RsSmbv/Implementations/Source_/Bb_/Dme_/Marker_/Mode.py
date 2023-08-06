from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.AvionicMarkMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:[BB]:DME:MARKer<CH>:MODE \n
		Sets the mode for the selected marker. \n
			:param mode: FPSTart| FP50P| PSTart| P50P| PRECeived FPSTart: first pulse start FP50: first pulse 50% PSTart: pulse start P50: pulse 50% PRECeived: received pulse
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicMarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:MARKer{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.AvionicMarkMode:
		"""[SOURce<HW>]:[BB]:DME:MARKer<CH>:MODE \n
		Sets the mode for the selected marker. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')
			:return: mode: FPSTart| FP50P| PSTart| P50P| PRECeived FPSTart: first pulse start FP50: first pulse 50% PSTart: pulse start P50: pulse 50% PRECeived: received pulse"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DME:MARKer{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicMarkMode)
