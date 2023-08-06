from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voltage:
	"""Voltage commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("voltage", core, parent)

	def set(self, voltage: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:LFOutput<CH>:INTernal:VOLTage \n
		Sets the output voltage for the LF generators. The sum of both values must not exceed the overall output voltage, set
		with command [:SOURce]:LFOutput:VOLTage. \n
			:param voltage: float Range: 0 to 4
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')"""
		param = Conversions.decimal_value_to_str(voltage)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:LFOutput{channel_cmd_val}:INTernal:VOLTage {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce]:LFOutput<CH>:INTernal:VOLTage \n
		Sets the output voltage for the LF generators. The sum of both values must not exceed the overall output voltage, set
		with command [:SOURce]:LFOutput:VOLTage. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')
			:return: voltage: float Range: 0 to 4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:LFOutput{channel_cmd_val}:INTernal:VOLTage?')
		return Conversions.str_to_float(response)
