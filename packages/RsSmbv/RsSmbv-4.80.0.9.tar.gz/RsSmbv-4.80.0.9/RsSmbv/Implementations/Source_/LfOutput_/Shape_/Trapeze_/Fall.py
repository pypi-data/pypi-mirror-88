from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fall:
	"""Fall commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fall", core, parent)

	def set(self, fall: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:LFOutput<CH>:SHAPe:TRAPeze:FALL \n
		Selects the fall time for the trapezoid shape of the LF generator. \n
			:param fall: float Range: 1E-6 to 100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')"""
		param = Conversions.decimal_value_to_str(fall)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput{channel_cmd_val}:SHAPe:TRAPeze:FALL {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:LFOutput<CH>:SHAPe:TRAPeze:FALL \n
		Selects the fall time for the trapezoid shape of the LF generator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')
			:return: fall: float Range: 1E-6 to 100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:LFOutput{channel_cmd_val}:SHAPe:TRAPeze:FALL?')
		return Conversions.str_to_float(response)
