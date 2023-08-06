from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CndRatio:
	"""CndRatio commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cndRatio", core, parent)

	def set(self, cn_density_ratio: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:CNDRatio \n
		Sets the carrier power to noise power ratio C/N ratio, that is the difference of carrier power and noise power: C/N ratio
		= Carrier power - Noise power Noise power = Refrence power + 10 * log10(System Bandwidth) - C/ N0 \n
			:param cn_density_ratio: float Range: 0 to 55
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(cn_density_ratio)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:CNDRatio {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:CNDRatio \n
		Sets the carrier power to noise power ratio C/N ratio, that is the difference of carrier power and noise power: C/N ratio
		= Carrier power - Noise power Noise power = Refrence power + 10 * log10(System Bandwidth) - C/ N0 \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: cn_density_ratio: float Range: 0 to 55"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:CNDRatio?')
		return Conversions.str_to_float(response)
