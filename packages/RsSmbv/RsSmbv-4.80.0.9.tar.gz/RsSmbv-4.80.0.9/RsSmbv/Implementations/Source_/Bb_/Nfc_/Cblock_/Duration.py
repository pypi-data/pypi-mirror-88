from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Duration:
	"""Duration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("duration", core, parent)

	def set(self, duration: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:DURation \n
		Determines the frame period in µs. \n
			:param duration: float Range: 0 to 1E6
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.decimal_value_to_str(duration)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DURation {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:DURation \n
		Determines the frame period in µs. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: duration: float Range: 0 to 1E6"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DURation?')
		return Conversions.str_to_float(response)
