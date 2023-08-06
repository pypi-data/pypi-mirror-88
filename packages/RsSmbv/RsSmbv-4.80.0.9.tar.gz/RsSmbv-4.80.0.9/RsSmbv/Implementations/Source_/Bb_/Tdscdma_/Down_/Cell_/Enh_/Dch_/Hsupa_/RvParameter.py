from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RvParameter:
	"""RvParameter commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rvParameter", core, parent)

	def set(self, rv_parameter: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:RVParameter \n
		(for HARQ Mode set to constant ACK) Sets the redundancy version parameter, i.e. indicates which redundancy version of the
		data is sent. \n
			:param rv_parameter: integer Range: 0 to 7
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(rv_parameter)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSUPA:RVParameter {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:RVParameter \n
		(for HARQ Mode set to constant ACK) Sets the redundancy version parameter, i.e. indicates which redundancy version of the
		data is sent. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: rv_parameter: integer Range: 0 to 7"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSUPA:RVParameter?')
		return Conversions.str_to_int(response)
