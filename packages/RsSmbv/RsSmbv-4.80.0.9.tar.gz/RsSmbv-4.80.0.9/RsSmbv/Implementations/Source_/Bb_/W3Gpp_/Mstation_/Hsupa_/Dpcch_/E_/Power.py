from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def set(self, power: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:POWer \n
		The command sets the power of the E-DPCCH channel. \n
			:param power: float Range: -80 dB to 0 dB
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(power)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:POWer {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:POWer \n
		The command sets the power of the E-DPCCH channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: power: float Range: -80 dB to 0 dB"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:POWer?')
		return Conversions.str_to_float(response)
