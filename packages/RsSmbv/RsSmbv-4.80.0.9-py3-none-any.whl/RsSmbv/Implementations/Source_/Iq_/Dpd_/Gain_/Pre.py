from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pre:
	"""Pre commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pre", core, parent)

	def set(self, pre_gain: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DPD<ST>:GAIN:PRE \n
		Sets a pre-gain (i.e. an attenuation) to define the range the static DPD is applied in. \n
			:param pre_gain: float Range: -50 to 20
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.decimal_value_to_str(pre_gain)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:GAIN:PRE {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:IQ:DPD<ST>:GAIN:PRE \n
		Sets a pre-gain (i.e. an attenuation) to define the range the static DPD is applied in. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: pre_gain: float Range: -50 to 20"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:GAIN:PRE?')
		return Conversions.str_to_float(response)
