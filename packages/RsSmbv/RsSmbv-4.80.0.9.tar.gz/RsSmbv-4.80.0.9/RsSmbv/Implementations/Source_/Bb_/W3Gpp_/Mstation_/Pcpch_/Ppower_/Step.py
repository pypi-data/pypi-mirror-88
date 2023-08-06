from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	def set(self, step: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:PPOWer:STEP \n
		The command defines the step width of the power increase, by which the preamble component of the PCPCH is increased from
		repetition to repetition. The power during the last repetition corresponds to the power defined by the command method
		RsSmbv.Source.Bb.W3Gpp.Mstation.Pcpch.Ppower.set. \n
			:param step: float Range: 0 dB to 10 dB
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(step)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:PPOWer:STEP {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:PPOWer:STEP \n
		The command defines the step width of the power increase, by which the preamble component of the PCPCH is increased from
		repetition to repetition. The power during the last repetition corresponds to the power defined by the command method
		RsSmbv.Source.Bb.W3Gpp.Mstation.Pcpch.Ppower.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: step: float Range: 0 dB to 10 dB"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:PPOWer:STEP?')
		return Conversions.str_to_float(response)
