from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class JsRatio:
	"""JsRatio commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("jsRatio", core, parent)

	def set(self, js_ratio: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:JSRatio \n
		Sets the jammer (interferer) power to signal power ratio C/I ratio, that is the difference of carrier power and noise
		power: C/I ratio = Carrier power - Interferer power Interferer power = Refrence power + J/S \n
			:param js_ratio: float Range: -50 to 50
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(js_ratio)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:JSRatio {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:JSRatio \n
		Sets the jammer (interferer) power to signal power ratio C/I ratio, that is the difference of carrier power and noise
		power: C/I ratio = Carrier power - Interferer power Interferer power = Refrence power + J/S \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: js_ratio: float Range: -50 to 50"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:JSRatio?')
		return Conversions.str_to_float(response)
