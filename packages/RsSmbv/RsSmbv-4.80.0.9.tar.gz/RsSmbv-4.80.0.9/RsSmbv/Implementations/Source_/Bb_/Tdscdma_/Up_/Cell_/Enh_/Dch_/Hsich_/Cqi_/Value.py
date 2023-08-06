from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Value:
	"""Value commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("value", core, parent)

	def set(self, value: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:HSICh:CQI:VALue \n
		Sets the CQI value. \n
			:param value: integer Range: 0 to 63
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(value)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:HSICh:CQI:VALue {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:HSICh:CQI:VALue \n
		Sets the CQI value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: value: integer Range: 0 to 63"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:HSICh:CQI:VALue?')
		return Conversions.str_to_int(response)
