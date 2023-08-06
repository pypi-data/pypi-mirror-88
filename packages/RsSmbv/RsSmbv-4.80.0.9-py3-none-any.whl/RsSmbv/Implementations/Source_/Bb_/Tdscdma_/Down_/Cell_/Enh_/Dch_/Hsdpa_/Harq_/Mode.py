from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.EnhHsHarqMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:HARQ:MODE \n
		Sets the HARQ simulation mode. \n
			:param mode: CACK| CNACk CACK New data is used for each new TTI. This mode is used to simulate maximum throughput transmission. CNACk Enables NACK simulation, i.e. depending on the sequence selected with command BB:TDSC:DOWN:CELL1:ENH:DCH:HSDPA:RVS packets are retransmitted. This mode is used for testing with varying redundancy version.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(mode, enums.EnhHsHarqMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSDPA:HARQ:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EnhHsHarqMode:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:HARQ:MODE \n
		Sets the HARQ simulation mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: mode: CACK| CNACk CACK New data is used for each new TTI. This mode is used to simulate maximum throughput transmission. CNACk Enables NACK simulation, i.e. depending on the sequence selected with command BB:TDSC:DOWN:CELL1:ENH:DCH:HSDPA:RVS packets are retransmitted. This mode is used for testing with varying redundancy version."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSDPA:HARQ:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EnhHsHarqMode)
