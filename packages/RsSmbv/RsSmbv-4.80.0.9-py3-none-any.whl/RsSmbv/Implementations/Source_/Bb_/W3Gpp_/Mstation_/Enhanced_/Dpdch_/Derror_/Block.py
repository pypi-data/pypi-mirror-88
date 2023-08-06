from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Block:
	"""Block commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("block", core, parent)

	def get_rate(self) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:DERRor:BLOCk:RATE \n
		Sets the block error rate. \n
			:return: rate: float Range: 1E-4 to 0.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DERRor:BLOCk:RATE?')
		return Conversions.str_to_float(response)

	def set_rate(self, rate: float) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:DERRor:BLOCk:RATE \n
		Sets the block error rate. \n
			:param rate: float Range: 1E-4 to 0.5
		"""
		param = Conversions.decimal_value_to_str(rate)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DERRor:BLOCk:RATE {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:DERRor:[BLOCk]:STATe \n
		The command activates or deactivates block error generation. Block error generation is only possible when channel coding
		is activated. During block error generation, the CRC checksum is determined and then the last bit is inverted at the
		specified error probability in order to simulate a defective signal. \n
			:return: state: ON| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DERRor:BLOCk:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:DERRor:[BLOCk]:STATe \n
		The command activates or deactivates block error generation. Block error generation is only possible when channel coding
		is activated. During block error generation, the CRC checksum is determined and then the last bit is inverted at the
		specified error probability in order to simulate a defective signal. \n
			:param state: ON| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DERRor:BLOCk:STATe {param}')
