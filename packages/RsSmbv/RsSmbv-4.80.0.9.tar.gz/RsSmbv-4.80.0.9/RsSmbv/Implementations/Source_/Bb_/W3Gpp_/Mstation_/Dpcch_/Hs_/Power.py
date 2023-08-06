from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def set(self, power: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:POWer \n
		Sets the channel power in dB. The power is set relative to the powers of the other channels. If 'Adjust Total Power to 0
		dB' is executed (method RsSmbv.Source.Bb.W3Gpp.Power.Adjust.set) , the power is normalized to total power for all
		channels of 0 dB. The power ratio of the individual channels remains unchanged. \n
			:param power: float Range: -80 to 0
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(power)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:POWer {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:POWer \n
		Sets the channel power in dB. The power is set relative to the powers of the other channels. If 'Adjust Total Power to 0
		dB' is executed (method RsSmbv.Source.Bb.W3Gpp.Power.Adjust.set) , the power is normalized to total power for all
		channels of 0 dB. The power ratio of the individual channels remains unchanged. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: power: float Range: -80 to 0"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:POWer?')
		return Conversions.str_to_float(response)
